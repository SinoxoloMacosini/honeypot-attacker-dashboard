"""
Generates PNG charts from honeypot logs:
- Top attacking IPs
- Most common username/password combos
- Attempts over time
"""

import json
import pandas as pd
import matplotlib.pyplot as plt

LOG_FILE = "logs/attempts.jsonl"
OUTPUT_DIR = "dashboard/static"


def load_logs():
    records = []
    with open(LOG_FILE, "r") as f:
        for line in f:
            records.append(json.loads(line))
    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def plot_top_ips(df):
    top_ips = df["source_ip"].value_counts().head(10)
    top_ips.plot(kind="bar", title="Top Attacking IPs")
    plt.xlabel("IP Address")
    plt.ylabel("Attempts")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/top_ips.png")
    plt.clf()


def plot_attempts_over_time(df):
    df.set_index("timestamp").resample("1H").size().plot(
        title="Attack Attempts Over Time"
    )
    plt.xlabel("Time")
    plt.ylabel("Number of Events")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/attempts_over_time.png")
    plt.clf()


if __name__ == "__main__":
    df = load_logs()
    plot_top_ips(df)
    plot_attempts_over_time(df)
    print("Charts saved to", OUTPUT_DIR)
