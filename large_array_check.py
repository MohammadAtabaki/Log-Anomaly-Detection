import pandas as pd
import json
import re

def detect_large_json_arrays(df_logs_parsed, array_length_threshold=500):
    """
    Scan logs that contain 'Received event result from database' and detect
    embedded JSON arrays with more than `array_length_threshold` items.
    
    Returns a DataFrame with trace_id, timestamp, key name, and array length.
    """
    df_received_events = df_logs_parsed[
        df_logs_parsed['line.message'].str.contains("Received event result from database", na=False)
    ].copy()

    oversized_arrays = []

    for idx, row in df_received_events.iterrows():
        msg = row['line.message']
        trace_id = row.get('line.mdc.trace_id') or row.get('fields.TraceID') or 'UNKNOWN'
        timestamp = row.get('timestamp_raw', 'UNKNOWN')

        try:
            match = re.search(r"Received event result from database: ({.*})", msg)
            if not match:
                continue

            json_str = match.group(1)
            json_str = json_str.replace('\\"', '"').replace("\\'", "'")
            parsed_json = json.loads(json_str)

            for key, value in parsed_json.items():
                if isinstance(value, list) and len(value) > array_length_threshold:
                    oversized_arrays.append({
                        'trace_id': trace_id,
                        'timestamp': timestamp,
                        'array_key': key,
                        'array_length': len(value)
                    })

        except Exception:
            continue

    return pd.DataFrame(oversized_arrays)


def preview_large_arrays(df_oversized):
    """
    Preview oversized array details if any found.
    """
    if df_oversized.empty:
        print("✅ No oversized arrays found.")
    else:
        print("⚠️ Oversized arrays detected:")
        print(df_oversized.head())
