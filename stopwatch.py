import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
import os

def extract_stopwatch_tasks(df_logs_parsed, output_csv="output/task2_stopwatch_details.csv"):
    """
    Extract stopwatch logs and return a structured DataFrame with:
    trace_id, stopwatch_name, total_time_sec, subtask, subtask_time_sec, subtask_percent
    """
    df_stopwatch_logs = df_logs_parsed[df_logs_parsed['line.message'].str.contains("StopWatch", na=False)].copy()

    stopwatch_records = []

    for idx, row in df_stopwatch_logs.iterrows():
        msg = row['line.message']
        trace_id = row.get('line.mdc.trace_id') or row.get('fields.TraceID') or None
        if not trace_id:
            continue  # Skip if no trace ID

        try:
            header_match = re.search(r"StopWatch '(.*?)':\s*([0-9.eE+-]+) seconds", msg)
            if not header_match:
                continue

            stopwatch_name = header_match.group(1)
            total_time = float(header_match.group(2))

            subtask_lines = re.findall(r"([0-9.eE+-]+)\s+(\d+)%\s+(.*)", msg)
            for sec, pct, task in subtask_lines:
                stopwatch_records.append({
                    'trace_id': trace_id,
                    'stopwatch_name': stopwatch_name,
                    'total_time_sec': total_time,
                    'subtask': task.strip() if task.strip() else 'Unnamed Task',
                    'subtask_time_sec': float(sec),
                    'subtask_percent': int(pct)
                })
        except Exception:
            continue

    result_df = pd.DataFrame(stopwatch_records)

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    result_df.to_csv(output_csv, index=False)
    return result_df


def plot_stopwatch_analysis(df_stopwatch_tasks, save_dir="output/figures"):
    """
    Plot and save charts for stopwatch analysis.
    """
    os.makedirs(save_dir, exist_ok=True)

    # ✅ Total duration histogram
    plt.figure(figsize=(10, 6))
    sns.histplot(df_stopwatch_tasks['total_time_sec'], bins=30, kde=True)
    plt.xlabel("Total Execution Time (seconds)")
    plt.title("Distribution of Total Stopwatch Execution Times")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/task2_total_time_distribution.png")
    plt.close()

    # ✅ Top subtasks by max %
    top_subtasks = (
        df_stopwatch_tasks.groupby('subtask')['subtask_percent']
        .max().reset_index()
        .sort_values(by='subtask_percent', ascending=False)
        .head(15)
    )

    plt.figure(figsize=(12, 6))
    barplot = sns.barplot(y='subtask', x='subtask_percent', data=top_subtasks, palette="Blues_d")


    for bar in barplot.patches:
        width = bar.get_width()
        plt.text(width + 1, bar.get_y() + bar.get_height() / 2, f'{int(width)}%', va='center')

    plt.xlabel("Maximum % Time Spent")
    plt.ylabel("Subtask")
    plt.title("Top 15 Most Time-Consuming Subtasks by %")
    plt.tight_layout()
    plt.savefig(f"{save_dir}/task2_top_subtasks.png")
    plt.close()
