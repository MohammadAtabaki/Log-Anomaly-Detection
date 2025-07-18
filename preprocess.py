from load_and_parse import recursive_flatten
import json
import re
import pandas as pd




def classify_message(msg):
    if 'Executing stored procedure: EXEC P_MS_TF_ExecuteEvent' in msg:
        return 'EXECUTE_EVENT'
    elif "StopWatch 'execute event on file temp'" in msg:
        return 'STOPWATCH_EXECUTE_TEMP'
    elif 'StopWatch' in msg:
        return 'STOPWATCH_GENERIC'
    elif 'Received event result from database' in msg:
        return 'RECEIVED_EVENT_RESULT'
    elif 'Executing stored procedure' in msg:
        return 'OTHER_EXEC_PROC'
    else:
        return 'OTHER'

def parse_message_safely(msg):
    """Try to extract and flatten JSON content from the message string."""
    try:
        match = re.search(r'({.*})', msg, flags=re.DOTALL)
        if match:
            json_like = match.group(1).replace('\\"', '"').replace("\\'", "'")
            parsed = json.loads(json_like)
            return recursive_flatten(parsed)
    except Exception:
        pass
    return {}


def clean_logs(df_logs: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and enriches the log data:
    - Parses datetime
    - Drops noisy columns
    - Classifies messages
    - Parses line.message JSON into flat columns
    """
    # ✅ Parse datetime
    if "line.timestamp" in df_logs.columns:
        df_logs["line.timestamp"] = pd.to_datetime(df_logs["line.timestamp"], errors='coerce')

    # ✅ Drop noisy or unhelpful columns
    df_logs = df_logs.drop(columns=['line.mdc.errorId', 'line.exception', 'line.timestamp'], errors='ignore')

    # ✅ Drop single-value columns
    df_logs = df_logs.drop(columns=df_logs.columns[df_logs.nunique() == 1])

    # ✅ Drop manual noisy column
    df_logs = df_logs.drop(columns=['line.level'], errors='ignore')

    # ✅ Classify message type
    df_logs['message_type'] = df_logs['line.message'].fillna('').apply(classify_message)

    # ✅ Parse line.message JSON
    parsed_msgs = df_logs['line.message'].dropna().apply(parse_message_safely)
    flat_msg_df = pd.json_normalize(parsed_msgs)

    # ✅ Merge into final parsed log
    df_logs_parsed = pd.concat([df_logs.reset_index(drop=True), flat_msg_df], axis=1)

    return df_logs_parsed
