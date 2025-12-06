#!/usr/bin/env python3
"""
Simple TCP server for CYB333 socket assignment.

- Listens on localhost:5000
- Accepts a single client connection
- Receives messages and sends responses
- Handles errors and shuts down cleanly
"""

import socket
import sys
import time
from datetime import datetime

HOST = "127.0.0.1"   # Loopback address (localhost)
PORT = 5000          # Arbitrary non-privileged port
BUFFER_SIZE = 1024   # How many bytes to read at a time
ENCODING = "utf-8"   # String encoding
SERVER_START_TIME = time.time()  # Track server start time for uptime

# Command descriptions - single source of truth
COMMANDS = [
    ("time", "Get the current server time"),
    ("uptime", "Get server uptime"),
    ("help", "Display all commands"),
    ("exit", "Disconnect from the server"),
    ("(any text)", "Echo message back to you"),
]


def get_commands_text(prefix: str = "") -> str:
    """Generate formatted command list with given prefix."""
    lines = [prefix] if prefix else []
    for cmd, desc in COMMANDS:
        lines.append(f"{cmd:<10}: {desc}")
    return "\n".join(lines)


def receive_message(conn: socket.socket) -> str | None:
    """
    Receive and decode a message from client.
    Returns decoded message or None if connection closed.
    """
    try:
        data = conn.recv(BUFFER_SIZE)
    except ConnectionResetError:
        print("[!] Connection reset by client.")
        return None

    if not data:
        print("[*] Client closed the connection.")
        return None

    return data.decode(ENCODING).strip()


def send_response(conn: socket.socket, response: str) -> bool:
    """
    Send response to client.
    Returns True on success, False on failure.
    """
    try:
        conn.sendall((response + "\n").encode(ENCODING))
        print(f"[>] [Sent to client] {response}")
        return True
    except BrokenPipeError:
        print("[!] Failed to send data. Client may have disconnected.")
        return False


def handle_message(conn: socket.socket, message: str) -> bool:
    """
    Process client message and send appropriate response.
    Returns False if client requested exit or connection failed, True to continue.
    """
    print(f"[<] [Received from client] {message}")

    if message.lower() == "exit":
        goodbye = "Goodbye from server."
        send_response(conn, goodbye)
        print("[*] Client requested to close the connection. Shutting down.")
        return False

    if message.lower() == "help":
        help_text = get_commands_text("\n--- Available Commands ---")
        if not send_response(conn, help_text):
            return False
        return True

    if message.lower() == "time":
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = f"[Current server time] {current_time}"
        if not send_response(conn, response):
            return False
        return True

    if message.lower() == "uptime":
        uptime_seconds = int(time.time() - SERVER_START_TIME)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        response = f"[Server uptime] {hours}h {minutes}m {seconds}s"
        if not send_response(conn, response):
            return False
        return True

    response = f"Server received \"{message}\""
    if not send_response(conn, response):
        return False

    return True


def handle_client(conn: socket.socket, addr: tuple) -> None:
    """
    Main loop for handling a connected client.
    """
    ip, port = addr
    print(f"[+] Connection established with {ip}:{port}")

    while True:
        message = receive_message(conn)
        if message is None:
            break

        if not handle_message(conn, message):
            break


def start_server() -> None:
    """Create, bind, and run the TCP server."""
    # Create a TCP/IP socket (AF_INET = IPv4, SOCK_STREAM = TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        # Allow reusing the address quickly after restart
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server_sock.bind((HOST, PORT))
        except OSError as exc:
            print(f"[!] Failed to bind to {HOST}:{PORT}: {exc}")
            sys.exit(1)

        # Start listening for incoming connections
        server_sock.listen()
        print(f"[+] Server listening on {HOST}:{PORT} ...")

        try:
            # Block until a client connects
            conn, addr = server_sock.accept()
            query_list(conn)
        except KeyboardInterrupt:
            print("\n[!] Server interrupted before accepting a connection. Shutting down.")
            return

        # Use context manager so the connection is closed automatically
        with conn:
            handle_client(conn, addr)

        print("[*] Server shut down cleanly.")

def query_list(conn: socket.socket) -> None:
    """
    Send welcome message and list of available commands to the client.
    """
    commands_list = get_commands_text("Available commands")
    welcome_message = f"\nWelcome to the server!\n----------------------\n{commands_list}\n----------------------\n"
    conn.sendall(welcome_message.encode(ENCODING))

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        # Catch Ctrl+C while server is running
        print("\n[!] Server interrupted by user. Exiting...")
