import os
import warnings
import joblib
from joblib import load
import matplotlib.pyplot as plt
import pandas as pd
warnings.filterwarnings("ignore")

from load_and_parse import load_all_logs
from preprocess import clean_logs
from global_stats import analyze_execute_event_flat, analyze_execute_event_hierarchy, plot_execute_event_combinations
from stopwatch import extract_stopwatch_tasks, plot_stopwatch_analysis
from large_array_check import detect_large_json_arrays
from eda import (
    summarize_columns, group_columns_by_prefix, plot_log_volume_over_time,
    plot_status_and_loggers, extract_top_keywords
)
from task2_anomaly_features import build_stopwatch_features
from anomaly_detection import run_isolation_forest, plot_anomaly_scores
from feature_engineering import process as feature_engineering_process
from dbscan_clustering import run_dbscan_clustering, plot_dbscan_clusters
from anomaly_detection_vs_dbscan import compare_dbscan_and_anomaly

TEST_DATA_DIR = "test_data"
TEST_RESULT_DIR = "test_result"
os.makedirs(TEST_RESULT_DIR, exist_ok=True)
os.makedirs(os.path.join(TEST_RESULT_DIR, "figures"), exist_ok=True)

# 1. Load and parse logs
logs = load_all_logs(TEST_DATA_DIR)

# 2. Clean logs
cleaned_logs = clean_logs(logs)

# 3. Task 1: Field analysis
analyze_execute_event_flat(cleaned_logs, output_csv=os.path.join(TEST_RESULT_DIR, "task1_global_field_combination.csv"))
analyze_execute_event_hierarchy(cleaned_logs, output_csv=os.path.join(TEST_RESULT_DIR, "task1_hierarchy_field_combination.csv"))
plot_execute_event_combinations(cleaned_logs, save_dir=os.path.join(TEST_RESULT_DIR, "figures"))

# 4. Task 2: Stopwatch analysis
stopwatch_df = extract_stopwatch_tasks(cleaned_logs, output_csv=os.path.join(TEST_RESULT_DIR, "task2_stopwatch_details.csv"))
plot_stopwatch_analysis(stopwatch_df, save_dir=os.path.join(TEST_RESULT_DIR, "figures"))

# 5. Task 3: Large array detection
detect_large_json_arrays(cleaned_logs)

# 6. EDA
summarize_columns(cleaned_logs, output_csv=os.path.join(TEST_RESULT_DIR, "eda_column_summary.csv"))
group_columns_by_prefix(cleaned_logs)
plot_log_volume_over_time(cleaned_logs, save_dir=os.path.join(TEST_RESULT_DIR, "figures"))
plot_status_and_loggers(cleaned_logs, save_dir=os.path.join(TEST_RESULT_DIR, "figures"))
extract_top_keywords(cleaned_logs, save_dir=TEST_RESULT_DIR)

# 7. Build features for anomaly detection (Isolation Forest)
features_df = build_stopwatch_features(
    input_path=os.path.join(TEST_RESULT_DIR, "task2_stopwatch_details.csv"),
    output_csv=os.path.join(TEST_RESULT_DIR, "task2_stopwatch_features.csv")
)
# 8. Predict anomalies using trained Isolation Forest
# Use run_isolation_forest with a model_path to load the trained model (not retrain)


# Load features
anomaly_features_path = os.path.join(TEST_RESULT_DIR, "task2_stopwatch_features.csv")
df_features = pd.read_csv(anomaly_features_path)
X = df_features[['total_time_sec', 'max_subtask_percent', 'sum_other_subtask_time', 'ratio_other_to_max']].copy()

# Load trained model
model = load("output/isolation_forest_model.joblib")
df_features['anomaly_score'] = model.predict(X)
df_features['anomaly_score_value'] = model.decision_function(X)
df_features['is_anomaly'] = df_features['anomaly_score'] == -1

# Save results
anomaly_results_path = os.path.join(TEST_RESULT_DIR, "anomaly_results.csv")
anomalies_detected_path = os.path.join(TEST_RESULT_DIR, "anomalies_detected.csv")
df_features.to_csv(anomaly_results_path, index=False)
df_features[df_features['is_anomaly']].to_csv(anomalies_detected_path, index=False)

# Plot anomaly scores (no show)
plot_anomaly_scores(df_features, save_dir=os.path.join(TEST_RESULT_DIR, "figures"))

# 9. Feature engineering for DBSCAN
feature_engineering_process(
    input_csv=os.path.join(TEST_RESULT_DIR, "task2_stopwatch_features.csv"),
    output_csv=os.path.join(TEST_RESULT_DIR, "preprocessed_clustering_features.csv"))

# 10. Predict clusters/anomalies using trained DBSCAN

dbscan_info = joblib.load("output/dbscan_model.joblib")
df_dbscan = pd.read_csv(os.path.join(TEST_RESULT_DIR, "preprocessed_clustering_features.csv"))
X_dbscan = df_dbscan[dbscan_info['feature_columns']]
labels = dbscan_info['model'].fit_predict(X_dbscan)
df_dbscan['cluster'] = labels
dbscan_results_path = os.path.join(TEST_RESULT_DIR, "dbscan_clustering_results.csv")
df_dbscan.to_csv(dbscan_results_path, index=False)

# Plot DBSCAN clusters (no show)
plot_dbscan_clusters(df_dbscan, save_dir=os.path.join(TEST_RESULT_DIR, "figures"))

# 11. Compare anomalies detected by both models
compare_dbscan_and_anomaly(csv_dbscan=dbscan_results_path, csv_anomaly=anomaly_results_path, output_dir=TEST_RESULT_DIR)

