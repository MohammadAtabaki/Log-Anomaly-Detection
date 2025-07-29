import pandas as pd
import matplotlib.pyplot as plt
import os

def compare_dbscan_and_anomaly(csv_dbscan="output/dbscan_clustering_results.csv", 
                               csv_anomaly="output/anomaly_results.csv",output_dir="output"):
    """
    Compare DBSCAN and Isolation Forest anomaly detection results based on trace_id and stopwatch_name.
    Identifies the following:
    1. Same anomalies detected by both models.
    2. Anomalies detected by Isolation Forest but not by DBSCAN.
    3. Anomalies detected by DBSCAN but not by Isolation Forest.
    """
    
    # Step 1: Load the DBSCAN and Anomaly Detection results
    dbscan_df = pd.read_csv(csv_dbscan)
    anomaly_df = pd.read_csv(csv_anomaly)
    
    print(f"✅ Loaded DBSCAN results: {dbscan_df.shape}")
    print(f"✅ Loaded Anomaly Detection results: {anomaly_df.shape}")

    # Step 2: Filter anomalies from both models
    dbscan_anomalies = dbscan_df[dbscan_df['cluster'] == -1]  # DBSCAN anomalies are labeled as -1
    isolation_forest_anomalies = anomaly_df[anomaly_df['is_anomaly'] == True]  # Isolation Forest anomalies
    
    print(f"✅ DBSCAN Anomalies: {dbscan_anomalies.shape[0]}")
    print(f"✅ Isolation Forest Anomalies: {isolation_forest_anomalies.shape[0]}")

    # Step 3: Initialize a list to store results
    final_comparison = []

    # Step 4: Compare anomalies from Isolation Forest with DBSCAN
    for idx, anomaly_row in isolation_forest_anomalies.iterrows():
        trace_id = anomaly_row['trace_id']
        stopwatch_name = anomaly_row['stopwatch_name']

        # Compare both trace_id and stopwatch_name to ensure correct matching
        dbscan_row = dbscan_anomalies[(dbscan_anomalies['trace_id'] == trace_id) & 
                                      (dbscan_anomalies['stopwatch_name'] == stopwatch_name)]
        
        if not dbscan_row.empty:
            # If there's a match, compare anomalies detected by both models
            dbscan_is_anomaly = dbscan_row['cluster'].values[0] == -1
            isolation_forest_is_anomaly = anomaly_row['is_anomaly'] == True

            final_comparison.append({
                'trace_id': trace_id,
                'stopwatch_name': stopwatch_name,
                'dbscan_is_anomaly': dbscan_is_anomaly,
                'isolation_forest_is_anomaly': isolation_forest_is_anomaly,
                'total_time_sec': anomaly_row['total_time_sec'],
                'max_subtask_percent': anomaly_row['max_subtask_percent'],
                'sum_other_subtask_time': anomaly_row['sum_other_subtask_time'],
                'ratio_other_to_max': anomaly_row['ratio_other_to_max'],
                'detected_by_both_models': dbscan_is_anomaly and isolation_forest_is_anomaly
            })
        
        else:
            # If no match in DBSCAN, the anomaly is only detected by Isolation Forest
            final_comparison.append({
                'trace_id': trace_id,
                'stopwatch_name': stopwatch_name,
                'dbscan_is_anomaly': False,
                'isolation_forest_is_anomaly': True,
                'total_time_sec': anomaly_row['total_time_sec'],
                'max_subtask_percent': anomaly_row['max_subtask_percent'],
                'sum_other_subtask_time': anomaly_row['sum_other_subtask_time'],
                'ratio_other_to_max': anomaly_row['ratio_other_to_max'],
                'detected_by_both_models': False
            })

    # Step 5: Compare anomalies for DBSCAN that are not in Isolation Forest
    for idx, dbscan_row in dbscan_anomalies.iterrows():
        trace_id = dbscan_row['trace_id']
        stopwatch_name = dbscan_row['stopwatch_name']

        # Check if the pair (trace_id, stopwatch_name) does not exist in Isolation Forest anomalies
        match = isolation_forest_anomalies[
            (isolation_forest_anomalies['trace_id'] == trace_id) &
            (isolation_forest_anomalies['stopwatch_name'] == stopwatch_name)
        ]
        if match.empty:
            final_comparison.append({
                'trace_id': trace_id,
                'stopwatch_name': stopwatch_name,
                'dbscan_is_anomaly': True,
                'isolation_forest_is_anomaly': False,
                'total_time_sec': dbscan_row['total_time_sec'],
                'max_subtask_percent': dbscan_row['max_subtask_percent'],
                'sum_other_subtask_time': dbscan_row['sum_other_subtask_time'],
                'ratio_other_to_max': dbscan_row['ratio_other_to_max'],
                'detected_by_both_models': False
            })

    # Step 6: Create DataFrame from the comparison
    comparison_df = pd.DataFrame(final_comparison)
    print(f"✅ Comparison DataFrame created with shape: {comparison_df.shape}")

    # 🔎 Preview: Show the number of anomalies in each category
    num_both = comparison_df['detected_by_both_models'].sum()
    num_isolation = comparison_df['isolation_forest_is_anomaly'].sum() - num_both
    num_dbscan = comparison_df['dbscan_is_anomaly'].sum() - num_both

    print("🔎 Anomaly detection preview:")
    print(f"Same anomalies detected by both models: {num_both}")
    print(f"Anomalies detected only by Isolation Forest: {num_isolation}")
    print(f"Anomalies detected only by DBSCAN: {num_dbscan}")

    # Step 7: Save the comparison DataFrame to CSV
    os.makedirs(output_dir, exist_ok=True)
    comparison_df.to_csv(os.path.join(output_dir, "dbscan_vs_isolation_forest_comparison.csv"), index=False)
    print(f"✅ Comparison results saved to output/dbscan_vs_isolation_forest_comparison.csv")

    # Step 8: Plot comparison results
    anomaly_counts = {
        'Same anomalies (both methods)': num_both,
        'Only Isolation Forest': num_isolation,
        'Only DBSCAN': num_dbscan
    }

    plt.figure(figsize=(8, 6))
    plt.bar(anomaly_counts.keys(), anomaly_counts.values(), color=['green', 'orange', 'red'])
    plt.title("Comparison of Anomalies Detected by DBSCAN and Isolation Forest")
    plt.ylabel("Number of Anomalies")
    plt.xlabel("Detection Method")
    plt.xticks(rotation=0)
    plt.tight_layout()

    # Save the comparison plot
    os.makedirs(os.path.join(output_dir, "figures"), exist_ok=True)
    plt.savefig(os.path.join(output_dir, "figures", "dbscan_vs_isolation_forest_comparison_plot.png"))
    print(f"🖼️ Comparison plot saved to output/figures/dbscan_vs_isolation_forest_comparison_plot.png")

    # Show the plot
    plt.show()

    return comparison_df
