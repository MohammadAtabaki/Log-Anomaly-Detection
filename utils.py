"""
main.py - Entry point to run log analysis
"""

import pandas as pd
from utils.parser import parse_message_safely
from log_analysis_project.utils.field_frequencies import analyze_field_frequencies
from utils.stopwatch_analysis import extract_stopwatch_data
from log_analysis_project.utils.large_fields import detect_large_arrays

def main(log_path):
    # Load JSON logs
    import json
    with open(log_path, 'r') as f:
        raw_logs = json.load(f)

    # Flatten logs
    flattened = [parse_message_safely(log['line']) for log in raw_logs]
    df = pd.DataFrame(flattened)

    # Task 1: Field Frequency
    print("🔍 Field Frequency Analysis:")
    print(analyze_field_frequencies(df).head())

    # Task 2: Stopwatch
    print("⏱️ Stopwatch Timing Breakdown:")
    print(extract_stopwatch_data(df).head())

    # Task 3: Large Arrays
    print("📦 Detect Large Arrays:")
    print(detect_large_arrays(df, threshold=500))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Usage: python main.py path_to_log_file.json")
