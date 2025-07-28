import pandas as pd
import os
import matplotlib.pyplot as plt
from load_and_parse import load_all_logs
from preprocess import clean_logs  

from global_stats import (
    analyze_execute_event_flat,
    analyze_execute_event_hierarchy, 
    plot_execute_event_combinations
)
from stopwatch import extract_stopwatch_tasks, plot_stopwatch_analysis
from large_array_check import detect_large_json_arrays
from eda import (
    summarize_columns,
    group_columns_by_prefix,
    plot_log_volume_over_time,
    plot_status_and_loggers,
    extract_top_keywords,
)

from task2_anomaly_features import build_stopwatch_features
from anomaly_detection import run_isolation_forest, plot_anomaly_scores

from anomaly_model_tester import load_model, generate_test_samples, test_model_on_samples
from feature_engineering import process as feature_engineering_process

from dbscan_clustering import run_dbscan_clustering, plot_dbscan_clusters
from anomaly_detection_vs_dbscan import compare_dbscan_and_anomaly

def save_result(df, filename):
    os.makedirs("output", exist_ok=True)
    df.to_csv(f"output/{filename}", index=False)

def save_plot(filename):
    os.makedirs("output/plots", exist_ok=True)
    plt.savefig(f"output/plots/{filename}", bbox_inches="tight")
    plt.close()


def main():
    # ✅ Step 1: Load raw logs
    print("📥 Loading and parsing logs...")
    df_logs = load_all_logs("data")
    print(f"✅ Loaded log shape: {df_logs.shape}")

    # ✅ Step 2: Clean and parse embedded message JSON
    print("🧹 Cleaning + Flattening embedded message JSON...")
    df_logs_parsed = clean_logs(df_logs)
    print(f"✅ Final parsed log shape: {df_logs_parsed.shape}")

    # ✅ Step 3: Run Task 1 - Global Field Combinations
    print("\n📊 Running Task 1: Occurrence Counts (Flat + Hierarchy)...")
    df_task1_1 =analyze_execute_event_flat(df_logs_parsed)
    print("\n🔍 Task 1 Method 1 Preview:")
    print(df_task1_1.head())
    save_result (df_task1_1, "task1_global_field_combination.csv")
    plot_execute_event_combinations(df_logs_parsed)

    print("\n📊 Running Hierarchy-aware analysis...")
    df_task1_2 = analyze_execute_event_hierarchy(df_logs_parsed)
    print("\n🔍 Task 1 Method 2 Preview:")
    print(df_task1_2.head())
    save_result (df_task1_2, "task1_global_field_combination.csv")

    # ✅ Step 4: Run Task 2 - Stopwatch Performance Analysis
    print("\n⏱️ Running Task 2: Stopwatch Timing Breakdown...")
    df_task2 = extract_stopwatch_tasks(df_logs_parsed)
    print("\n🔍 Task 2 Preview:")
    print(df_task2.head())
    save_result (df_task2, "task2_stopwatch_details.csv")

    plot_stopwatch_analysis(df_task2)
  

    # ✅ Step 5: Run Task 3 - Large Array Detection
    print("\n📦 Running Task 3: Large Array Detection...")
    detect_large_json_arrays(df_logs_parsed)

    # ✅ Step 6: Optional - EDA and Exploratory Insights
    print("\n🔎 Running EDA...")
    df_summarize = summarize_columns(df_logs_parsed)
    print(df_summarize.head())
    save_result(df_summarize, "eda_column_summary.csv")

    columns_by_prefix = group_columns_by_prefix(df_logs_parsed)
    print("\n🔍 Columns grouped by JSON prefix:")
    for prefix, count in columns_by_prefix.items():
        print(f"{prefix}: {count} columns")


    plot_log_volume_over_time(df_logs_parsed)


    plot_status_and_loggers(df_logs_parsed)


    extract_top_keywords(df_logs_parsed)


    print("\n✅ All tasks completed successfully!")

    # ✅ Step 7: Feature Extraction for Anomaly Detection

    print('Starting the task 2 stopwatch feature extraction for anomaly detection...')

    df_features = build_stopwatch_features()
    print(df_features.head())

    # ✅ Step 8: Anomaly Detection from Task 2 Features
    print("\n🚨 Running Anomaly Detection...")
    anomaly_df = run_isolation_forest("output/task2_stopwatch_features.csv")
    plot_anomaly_scores(anomaly_df)

    # Load the trained model
    model = load_model("output/isolation_forest_model.joblib")

    # Generate or load real test data (use generate_test_samples() if you want synthetic data)
    test_df = generate_test_samples()  # Or load your real data

    # Run the anomaly detection model
    results = test_model_on_samples(model, test_df)

    # Print the results
    print("Anomaly Detection Results:")
    print(results[['total_time_sec', 'max_subtask_percent', 'sum_other_subtask_time', 'ratio_other_to_max', 'prediction', 'anomaly_score']])


    # ✅ Step 9: Feature Engineering for KMeans clustering
    print("\n🔧 Running Feature Engineering for KMeans...")
    feature_engineering_process()

    print("✅ Feature engineering completed and saved.")


    # ✅ Step 10: DBSCAN Clustering
    print("\n🔍 Running DBSCAN Clustering...")
    dbscan_df = run_dbscan_clustering()
    print("✅ DBSCAN clustering completed and results saved.")
    plot_dbscan_clusters(dbscan_df)


    # ✅ Step 11: Compare DBSCAN and Anomaly Detection results
    print("\n🔍 Comparing DBSCAN and Anomaly Detection results...")
    compare_dbscan_and_anomaly()
    print("✅ Comparison completed and results saved.")
if __name__ == "__main__":
    main()
