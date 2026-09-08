"""
Basic SSH honeypot skeleton.
Listens on a port, accepts connections, and logs attempted
credentials without granting real access. For research/education only.
"""

import socket
import threading
import datetime

HOST = "0.0.0.0"
PORT = 2222  # non-privileged port for testing

def log_attempt(ip, data):
    timestamp = datetime.datetime.utcnow().isoformat()
    with open("logs.txt", "a") as f:
        f.write(f"{timestamp} | {ip} | {data}\n")

def handle_client(conn, addr):
    ip = addr[0]
    try:
        conn.send(b"SSH-2.0-OpenSSH_8.2\r\n")
        data = conn.recv(1024)
        log_attempt(ip, data)
    except Exception as e:
        log_attempt(ip, f"error: {e}")
    finally:
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Honeypot listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
