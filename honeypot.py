"""
SSH honeypot using paramiko to properly negotiate the SSH transport
and capture real auth attempts (username/password) instead of raw banners.
For research/education purposes only — no real login is ever granted.
"""

import socket
import threading
import paramiko
from logger import log_event, log_auth_attempt

HOST = "0.0.0.0"
PORT = 2222
HOST_KEY = paramiko.RSAKey.generate(2048)  # generated fresh each run for the demo


class HoneypotServer(paramiko.ServerInterface):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        log_auth_attempt(self.ip, self.port, username, password)
        return paramiko.AUTH_FAILED  # never actually let anyone in

    def get_allowed_auths(self, username):
        return "password"

    def check_channel_request(self, kind, chanid):
        return paramiko.OPEN_SUCCEEDED


def handle_client(client_sock, addr):
    ip, port = addr
    log_event(ip, port, "connection")
    try:
        transport = paramiko.Transport(client_sock)
        transport.add_server_key(HOST_KEY)
        server = HoneypotServer(ip, port)
        transport.start_server(server=server)

        chan = transport.accept(20)
        if chan is not None:
            chan.close()
    except Exception as e:
        log_event(ip, port, "error", {"message": str(e)})
    finally:
        log_event(ip, port, "disconnect")
        client_sock.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Honeypot listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()


if __name__ == "__main__":
    start_server()
