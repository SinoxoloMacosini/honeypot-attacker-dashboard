"""
Loads structured honeypot logs and produces basic attacker analytics.
This is the first pass — summary stats before visualization is added.
"""

import json
import pandas as pd

LOG_FILE = "logs/attempts.jsonl"

def load_logs():
    records = []
    with open(LOG_FILE, "r") as f:
        for line in f:
            records.append(json.loads(line))
    return pd.DataFrame(records)

def summarize(df):
    print("Total events:", len(df))
    print("\nTop source IPs:")
    print(df["source_ip"].value_counts().head(10))
    print("\nEvent type breakdown:")
    print(df["event_type"].value_counts())

if __name__ == "__main__":
    df = load_logs()
    summarize(df)
