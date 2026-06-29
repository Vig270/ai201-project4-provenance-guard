import json
from datetime import datetime

LOG_FILE = "audit_log.json"


def load_log():
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_log(logs):
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)


def add_entry(entry):
    logs = load_log()
    logs.append(entry)
    save_log(logs)
    return entry


def get_log():
    return load_log()[-10:]  # last 10 entries