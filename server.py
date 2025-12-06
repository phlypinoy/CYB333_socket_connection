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

HOST = "127.0.0.1"   # Loopback address (localhost)
PORT = 5000          # Arbitrary non-privileged port
BUFFER_SIZE = 1024   # How many bytes to read at a time
ENCODING = "utf-8"   # String encoding


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
        except KeyboardInterrupt:
            print("\n[!] Server interrupted before accepting a connection. Shutting down.")
            return

        # Use context manager so the connection is closed automatically
        with conn:
            ip, port = addr
            print(f"[+] Connection established with {ip}:{port}")

            while True:
                try:
                    data = conn.recv(BUFFER_SIZE)
                except ConnectionResetError:
                    print("[!] Connection reset by client.")
                    break

                # Empty data means the client closed the connection
                if not data:
                    print("[*] Client closed the connection.")
                    break

                message = data.decode(ENCODING).strip()
                print(f"[<] Received from client: {message}")

                # If client sends "exit", respond and then close
                if message.lower() == "exit":
                    goodbye = "Goodbye from server."
                    conn.sendall((goodbye + "\n").encode(ENCODING))
                    print(f"[>] Sent to client: {goodbye}")
                    print("[*] Client requested to close the connection. Shutting down.")
                    break

                # Normal response
                response = f"Server received: {message}"
                try:
                    conn.sendall((response + "\n").encode(ENCODING))
                    print(f"[>] Sent to client: {response}")
                except BrokenPipeError:
                    print("[!] Failed to send data. Client may have disconnected.")
                    break

        print("[*] Server shut down cleanly.")


if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        # Catch Ctrl+C while server is running
        print("\n[!] Server interrupted by user. Exiting...")
