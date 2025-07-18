# parser.py
import json
import re

def recursive_flatten(obj, parent_key='', sep='.'):
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

def parse_message_safely(msg):
    try:
        match = re.search(r'({.*})', msg, flags=re.DOTALL)
        if match:
            json_like = match.group(1).replace('\\"', '"').replace("\\'", "'")
            return recursive_flatten(json.loads(json_like))
    except:
        pass
    return {}
