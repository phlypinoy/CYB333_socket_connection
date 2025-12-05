#!/usr/bin/env python3
"""
Simple TCP client for CYB333 socket assignment.

- Connects to localhost:5000
- Sends user input to the server
- Prints server responses
- Handles errors when server is offline
- Supports a clean "exit" message to close connection
"""

import socket
import sys

HOST = "127.0.0.1"   # Server address (localhost)
PORT = 5000          # Must match the server port
BUFFER_SIZE = 1024
ENCODING = "utf-8"


def connect_to_server(host: str = HOST, port: int = PORT) -> None:
    """Connect to the TCP server and handle message exchange."""
    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Optional timeout so we don't hang forever on connect()
        sock.settimeout(5.0)

        # ----- Connection phase -----
        try:
            sock.connect((host, port))
        except ConnectionRefusedError:
            print(f"[!] Could not connect to server at {host}:{port} (connection refused). "
                  f"Is the server running?")
            return
        except socket.timeout:
            print(f"[!] Connection attempt to {host}:{port} timed out.")
            return
        except OSError as exc:
            print(f"[!] OS error while connecting: {exc}")
            return

        print(f"[+] Connected to server at {host}:{port}")
        print("Type messages and press Enter to send.")
        print('Type "exit" to close the connection cleanly.\n')

        # ----- Messaging phase -----
        try:
            while True:
                message = input("You: ")

                # Ignore empty lines instead of sending them
                if not message:
                    continue

                # Send the message to the server
                try:
                    sock.sendall((message + "\n").encode(ENCODING))
                except BrokenPipeError:
                    print("[!] Lost connection to the server while sending.")
                    break

                # If we send "exit", we expect a final server message then close
                if message.lower() == "exit":
                    try:
                        data = sock.recv(BUFFER_SIZE)
                    except OSError:
                        data = b""

                    if data:
                        print(f"Server: {data.decode(ENCODING).strip()}")

                    print("[*] Disconnected from server.")
                    break

                # Wait for the server response
                try:
                    data = sock.recv(BUFFER_SIZE)
                except ConnectionResetError:
                    print("[!] Connection reset by server.")
                    break

                if not data:
                    # Server closed the connection
                    print("[*] Server closed the connection.")
                    break

                print(f"Server: {data.decode(ENCODING).strip()}")

        except KeyboardInterrupt:
            print("\n[!] Client interrupted by user (Ctrl+C). Closing connection.")
            # Socket will be closed automatically by the context manager

        # When we leave the 'with' block, the socket is closed
        print("[*] Client shut down cleanly.")


if __name__ == "__main__":
    connect_to_server()
