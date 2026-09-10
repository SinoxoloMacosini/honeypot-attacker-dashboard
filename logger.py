"""
Structured logging for honeypot events.
Writes each connection attempt as a JSON line (JSONL) so the
dashboard can easily parse attacker behavior later.
"""

import json
import datetime
import os

LOG_FILE = "logs/attempts.jsonl"

def ensure_log_dir():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log_event(ip, port, event_type, details=None):
    ensure_log_dir()
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "source_ip": ip,
        "source_port": port,
        "event_type": event_type,   # e.g. "connection", "auth_attempt", "disconnect"
        "details": details or {}
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def log_auth_attempt(ip, port, username, password):
    log_event(ip, port, "auth_attempt", {
        "username": username,
        "password": password
    })
