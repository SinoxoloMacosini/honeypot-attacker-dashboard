"""
Basic SSH honeypot skeleton.
Listens on a port, accepts connections, and logs attempted
credentials without granting real access. For research/education only.
"""

import socket
import threading
from logger import log_event, log_auth_attempt

HOST = "0.0.0.0"
PORT = 2222  # non-privileged port for testing

def handle_client(conn, addr):
    ip, port = addr
    log_event(ip, port, "connection")
    try:
        conn.send(b"SSH-2.0-OpenSSH_8.2\r\n")
        data = conn.recv(1024)
        # Placeholder: real parsing of SSH auth packets would go here.
        # For now we log the raw banner exchange as a mock attempt.
        log_auth_attempt(ip, port, username="unknown", password=str(data))
    except Exception as e:
        log_event(ip, port, "error", {"message": str(e)})
    finally:
        log_event(ip, port, "disconnect")
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
