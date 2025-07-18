import os
import json
import pandas as pd
from typing import Union

# 📌 Utility: Recursively flatten a nested dictionary or list
def recursive_flatten(obj, parent_key='', sep='.'):
    """Flatten nested JSON/dict into dot notation"""
    items = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            items.extend(recursive_flatten(v, new_key, sep=sep).items())
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            new_key = f"{parent_key}[{i}]"
            items.extend(recursive_flatten(v, new_key, sep=sep).items())
    else:
        items.append((parent_key, obj))
    return dict(items)


# ✅ Main function to load and flatten all logs
def load_all_logs(data_folder="data"):
    raw_logs = []
    json_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.endswith(".json")]

    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
                raw_logs.extend(content)
                print(f"✅ Loaded {len(content)} records from {os.path.basename(file_path)}")
        except Exception as e:
            print(f"⚠️ Error reading {file_path}: {e}")

    all_flattened_logs = []

    for entry in raw_logs:
        flattened_entry = {}
        flattened_entry["timestamp_raw"] = entry.get("timestamp")

        if "fields" in entry:
            flattened_entry.update(recursive_flatten(entry["fields"], parent_key="fields"))

        try:
            line_data = json.loads(entry["line"])
            for key, value in line_data.items():
                if isinstance(value, str):
                    try:
                        parsed_inner = json.loads(value)
                        if isinstance(parsed_inner, dict):
                            flattened_entry.update(recursive_flatten(parsed_inner, parent_key=f"line.{key}"))
                        else:
                            flattened_entry[f"line.{key}"] = parsed_inner
                    except json.JSONDecodeError:
                        flattened_entry[f"line.{key}"] = value
                elif isinstance(value, dict):
                    flattened_entry.update(recursive_flatten(value, parent_key=f"line.{key}"))
                else:
                    flattened_entry[f"line.{key}"] = value
        except json.JSONDecodeError:
            flattened_entry["line_parse_error"] = entry.get("line")

        all_flattened_logs.append(flattened_entry)

    return pd.DataFrame(all_flattened_logs)
