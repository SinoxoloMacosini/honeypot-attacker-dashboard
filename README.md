# SSH Honeypot & Attacker Analytics Dashboard

Cybersecurity project for WeThinkCode — a low-interaction SSH honeypot 
that logs connection attempts, credentials tried, and source IPs, 
feeding a dashboard for behavior analysis.

## Goals
- Fake SSH service that accepts connections and logs attacker activity
- Capture: source IP, timestamp, username/password attempts, session duration
- Store logs in structured format (JSON/CSV)
- Analytics dashboard to visualize attack patterns (top IPs, common creds, frequency over time)

## Planned structure
- `honeypot.py` — core listener/fake SSH service
- `logger.py` — structured logging handler
- `dashboard/` — analytics/visualization code
- `logs/` — captured attacker data (gitignored in practice)
- `requirements.txt` — dependencies

## Status
🚧 In progress — built for educational/defensive research purposes only.
