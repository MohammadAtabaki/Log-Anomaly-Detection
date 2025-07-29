import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import os





# 1. Column Summary Stats (Top 30 Columns)
def summarize_columns(df,output_csv="output/eda_column_summary.csv"):
    summary = pd.DataFrame({
        'Column': df.columns,
        'Non-Null Count': df.notnull().sum().values,
        'Null %': df.isnull().mean().round(4) * 100,
        'Unique Values': df.nunique().values,
        'Sample Value': [
            df[col].dropna().iloc[0] if df[col].notna().any() else np.nan 
            for col in df.columns
        ]
    })
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    summary.to_csv(output_csv, index=False)
    return summary.sort_values('Null %').head(30)

# 2. Grouping Columns by JSON Prefix
def group_columns_by_prefix(df):
    prefix_map = defaultdict(list)
    for col in df.columns:
        prefix = col.split('.')[0] if '.' in col else 'root'
        prefix_map[prefix].append(col)
    return {k: len(v) for k, v in prefix_map.items()}


# 3. Log Volume Over Time
def plot_log_volume_over_time(df, save_dir="output/figures"):

    df_time = df.copy()
    ts_numeric = pd.to_numeric(df_time['timestamp_raw'], errors='coerce')
    df_time['timestamp_converted'] = pd.to_datetime(ts_numeric / 1e9, unit='s', errors='coerce')
    df_time = df_time.dropna(subset=['timestamp_converted'])

    df_time['date'] = df_time['timestamp_converted'].dt.date
    df_time['hour'] = df_time['timestamp_converted'].dt.hour

    # Logs per day
    plt.figure(figsize=(14, 4))
    df_time['date'].value_counts().sort_index().plot(kind='bar', color='steelblue')
    plt.title("Logs per Day")
    plt.ylabel("Log Count")
    plt.xlabel("Date")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/logs_per_day.png")
    plt.close()

    # Logs per hour
    plt.figure(figsize=(10, 4))
    df_time['hour'].value_counts().sort_index().plot(kind='bar', color='orange')
    plt.title("Logs per Hour")
    plt.ylabel("Log Count")
    plt.xlabel("Hour of Day")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/logs_per_hour.png")
    plt.close()

# 4. Status Fields and Logger Analysis
def plot_status_and_loggers(df, save_dir="output/figures"):
 

     # Detected levels
    plt.figure(figsize=(8, 4))
    df['fields.detected_level'].value_counts().plot(kind='bar', title="Detected Levels")
    plt.tight_layout()
    plt.savefig(f"{save_dir}/detected_levels.png")
    plt.close()


    # Top 15 logger classes
    plt.figure(figsize=(10, 6))
    df['line.logger'].value_counts().head(15).plot(kind='barh', title="Top 15 Logger Classes")
    plt.tight_layout()
    plt.savefig(f"{save_dir}/top_15_loggers.png")
    plt.close()

def extract_top_keywords(df, top_n=30, save_csv=True, save_dir="output"):


    corpus = df['line.message'].dropna().astype(str).values
    vectorizer = CountVectorizer(stop_words='english', max_features=top_n)
    X = vectorizer.fit_transform(corpus)

    keywords = pd.DataFrame(X.sum(axis=0), columns=vectorizer.get_feature_names_out()).T
    keywords.columns = ['Frequency']
    result = keywords.sort_values(by='Frequency', ascending=False)

    if save_csv:
        result.to_csv(f"{save_dir}/top_keywords.csv")

    return result