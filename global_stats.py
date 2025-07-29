import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import os

def analyze_execute_event_flat(df_logs_parsed, output_csv="output/task1_global_field_combination.csv"):
    """
    Extract and count combinations of [FileTypeID, EventID, FieldID, CommandID]
    from all columns in a flat way (regardless of hierarchy).
    """
    target_fields = ['FileTypeID', 'EventID', 'FieldID', 'CommandID']

    # 🔍 Find all columns containing each field name
    field_columns = {
        key: [col for col in df_logs_parsed.columns if key in col]
        for key in target_fields
    }

    # 🧱 Build flat combinations
    combinations = []
    for idx, row in df_logs_parsed.iterrows():
        entry = {}
        for key in target_fields:
            for col in field_columns[key]:
                val = row[col]
                if pd.notnull(val):
                    try:
                        entry[key] = int(val)
                        break
                    except (ValueError, TypeError):
                        continue
            if key not in entry:
                entry[key] = np.nan
        combinations.append(entry)

    # 📊 Create grouped dataframe
    df_combinations = pd.DataFrame(combinations)
    df_grouped = (
        df_combinations.groupby(target_fields, dropna=False)
        .size()
        .reset_index(name='count')
        .sort_values(by='count', ascending=False)
    )

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df_grouped.to_csv(output_csv, index=False)

    return df_grouped





def plot_execute_event_combinations(df_logs_parsed, records_per_plot=20, save_dir="output/figures"):
    """
    Visualize grouped ExecuteEvent combinations in bar chart subplots.
    Each group of 20 records is saved as a separate PNG file.
    """
    os.makedirs(save_dir, exist_ok=True)

    target_fields = ['FileTypeID', 'EventID', 'FieldID', 'CommandID']
    field_columns = {key: [col for col in df_logs_parsed.columns if key in col] for key in target_fields}
    combinations = []

    for idx, row in df_logs_parsed.iterrows():
        entry = {}
        for key in target_fields:
            for col in field_columns[key]:
                val = row[col]
                if pd.notnull(val):
                    try:
                        entry[key] = int(val)
                        break
                    except (ValueError, TypeError):
                        continue
            if key not in entry:
                entry[key] = float('nan')
        combinations.append(entry)

    df_combinations = pd.DataFrame(combinations)
    df_grouped = df_combinations.groupby(target_fields, dropna=False).size().reset_index(name='count')
    df_grouped = df_grouped.sort_values(by='count', ascending=False)

    # Filter out all-NaN rows and create labels
    df_grouped_no_nan = df_grouped[~(df_grouped[target_fields].isnull().all(axis=1))].copy()
    df_grouped_no_nan['label'] = df_grouped_no_nan.apply(
        lambda row: f"FT:{int(row['FileTypeID']) if pd.notnull(row['FileTypeID']) else 'NA'} | "
                    f"E:{int(row['EventID']) if pd.notnull(row['EventID']) else 'NA'} | "
                    f"F:{int(row['FieldID']) if pd.notnull(row['FieldID']) else 'NA'} | "
                    f"C:{int(row['CommandID']) if pd.notnull(row['CommandID']) else 'NA'}",
        axis=1
    )

    num_plots = math.ceil(len(df_grouped_no_nan) / records_per_plot)

    for i in range(num_plots):
        start_idx = i * records_per_plot
        end_idx = start_idx + records_per_plot
        subset = df_grouped_no_nan.iloc[start_idx:end_idx]

        fig, ax = plt.subplots(figsize=(16, 6))
        bars = ax.barh(subset['label'], subset['count'], color='skyblue')

        for bar in bars:
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height() / 2, str(int(width)), va='center')

        ax.set_xlabel("Count")
        ax.set_title(f"ExecuteEvent Combinations [{start_idx + 1}–{min(end_idx, len(df_grouped_no_nan))}]")
        ax.invert_yaxis()
        plt.tight_layout()

        plot_filename = f"{save_dir}/task1_combinations_{i+1}.png"
        plt.savefig(plot_filename)
        plt.close()


def analyze_execute_event_hierarchy(df_logs_parsed, output_csv="output/task1_hierarchy_field_combination.csv"):
    """
    Task 1 - Method 2:
    Count occurrences of CommandID, EventID, FieldID, and FileTypeID
    with respect to their exact JSON column path (hierarchy-aware).
    """
    target_fields = ['CommandID', 'EventID', 'FieldID', 'FileTypeID']
    hierarchy_data = []

    field_column_map = {
        key: [col for col in df_logs_parsed.columns if key in col]
        for key in target_fields
    }

    for field, columns in field_column_map.items():
        for col in columns:
            non_null_values = df_logs_parsed[col].dropna()
            for val in non_null_values:
                try:
                    val_int = int(val)
                    hierarchy_data.append((field, col, val_int))
                except (ValueError, TypeError):
                    continue

    df_hierarchy = pd.DataFrame(hierarchy_data, columns=['Field', 'JSON_Path', 'Value'])
    df_summary = (
        df_hierarchy
        .groupby(['Field', 'JSON_Path', 'Value'])
        .size()
        .reset_index(name='Count')
        .sort_values(by='Count', ascending=False)
    )
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df_summary.to_csv(output_csv, index=False)
    
    return df_summary
