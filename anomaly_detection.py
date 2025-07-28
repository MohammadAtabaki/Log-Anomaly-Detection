import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import os
import joblib

def run_isolation_forest(csv_path="output/task2_stopwatch_features.csv", contamination=0.01, random_state=42):
    """
    Load stopwatch features and apply Isolation Forest for anomaly detection.
    Saves results as CSV and plot in the 'output/' folder.
    """
    print("📦 Loading feature data...")
    df = pd.read_csv(csv_path)
    print(f"✅ Feature data shape: {df.shape}")

    # Drop rows with missing values in key features
    df = df.dropna(subset=['ratio_other_to_max'])


    # Feature matrix
    X = df[['total_time_sec', 'max_subtask_percent', 'sum_other_subtask_time', 'ratio_other_to_max']].copy()

    # Fit Isolation Forest
    print("🧠 Training Isolation Forest...")
    model = IsolationForest(n_estimators=100, contamination=contamination, random_state=random_state)
    df['anomaly_score'] = model.fit_predict(X)
    df['anomaly_score_value'] = model.decision_function(X)
    df['is_anomaly'] = df['anomaly_score'] == -1

    # Preview
    print("🔍 Anomalies Detected:", df['is_anomaly'].sum())
    print(df[df['is_anomaly']].head())

    # Create output folder if needed
    os.makedirs("output", exist_ok=True)

    # Save CSV
    df.to_csv("output/anomaly_results.csv", index=False)
    print("💾 Anomaly results saved to output/anomaly_results.csv")

    os.makedirs(os.path.dirname("output/isolation_forest_model.joblib"), exist_ok=True)
    joblib.dump(model, "output/isolation_forest_model.joblib")

    return df
def plot_anomaly_scores(df):

    # Plot and save figure
    plt.figure(figsize=(10, 6))
    colors = df['is_anomaly'].map({True: 'red', False: 'green'})
    plt.scatter(range(len(df)), df['anomaly_score_value'], c=colors, alpha=0.6)
    plt.title("Anomaly Score Distribution")
    plt.xlabel("Index")
    plt.ylabel("Anomaly Score (higher = more normal)")
    plt.axhline(y=0, color='black', linestyle='--', linewidth=1)
    plt.tight_layout()
    plt.savefig("output/figures/anomaly_scores.png")
    print("🖼️ Plot saved to output/anomaly_scores.png")
    plt.show()


    """
    Save the trained Isolation Forest model to a file.
    """
    





