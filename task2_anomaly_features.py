import pandas as pd
import os

def build_stopwatch_features(input_path="output/task2_stopwatch_details.csv"):
    """
    Build a feature table from stopwatch subtask breakdowns for anomaly detection.
    """
    # ✅ Step 1: Load stopwatch details CSV
    df = pd.read_csv(input_path)

    # ✅ Step 2: Identify the max subtask and summarize others per stopwatch
    groups = df.groupby(['trace_id', 'stopwatch_name'])
    feature_rows = []

    for (trace_id, stopwatch), group in groups:
        if group.empty:
            continue

        # Find the subtask with the highest percent
        top_row = group.loc[group['subtask_percent'].idxmax()]
        max_subtask = top_row['subtask']
        max_percent = top_row['subtask_percent']
        max_time = top_row['subtask_time_sec']
        total_time = top_row['total_time_sec']

        # Sum the remaining subtasks' time
        other_time = group['subtask_time_sec'].sum() - max_time

        feature_rows.append({
            'trace_id': trace_id,
            'stopwatch_name': stopwatch,
            'total_time_sec': total_time,
            'max_subtask': max_subtask,
            'max_subtask_percent': max_percent,
            'sum_other_subtask_time': other_time,
            'ratio_other_to_max': other_time / max_time if max_time else 0
        })

    df_features = pd.DataFrame(feature_rows)

    # ✅  Save to output folder
    os.makedirs("output", exist_ok=True)
    df_features.to_csv("output/task2_stopwatch_features.csv", index=False)
    print("✅ Feature table saved to output/task2_stopwatch_features.csv")

    return df_features
