#!/usr/bin/env python3
"""
CYB333 Socket Connection Project - Client

Refactored version with:
- Separate connect and messaging logic
- Clear error handling and shutdown path
"""

import socket
import sys

HOST = "127.0.0.1"   # Server address (localhost)
PORT = 5000          # Must match the server port
BUFFER_SIZE = 1024
ENCODING = "utf-8"
CONNECT_TIMEOUT = 5.0


def create_client_socket() -> socket.socket:
    """
    Create and return a TCP client socket with timeout configured.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(CONNECT_TIMEOUT)
    return sock


def connect_to_server(sock: socket.socket, host: str, port: int) -> bool:
    """
    Attempt to connect the client socket to the server.
    Returns True on success, False on failure.
    """
    try:
        sock.connect((host, port))
    except ConnectionRefusedError:
        print(f"[!] Could not connect to server at {host}:{port} (connection refused). "
              f"Is the server running?")
        return False
    except socket.timeout:
        print(f"[!] Connection attempt to {host}:{port} timed out.")
        return False
    except OSError as exc:
        print(f"[!] OS error while connecting: {exc}")
        return False

    print(f"[+] Connected to server at {host}:{port}")
    return True


def client_message_loop(sock: socket.socket) -> None:
    """
    Main loop: read user input, send to server, print responses.
    """
    print("Type messages and press Enter to send.")
    print('Type "exit" to close the connection cleanly.\n')

    try:
        while True:
            try:
                message = input("You: ")
            except EOFError:
                # e.g., Ctrl+D
                print("\n[!] EOF received. Closing client.")
                break

            if not message:
                # skip empty lines
                continue

            try:
                sock.sendall((message + "\n").encode(ENCODING))
            except BrokenPipeError:
                print("[!] Lost connection to the server while sending.")
                break

            if message.lower() == "exit":
                # Expect a final goodbye from server
                try:
                    data = sock.recv(BUFFER_SIZE)
                except OSError:
                    data = b""

                if data:
                    print(f"Server: {data.decode(ENCODING).strip()}")

                print("[*] Disconnected from server by request.")
                break

            # Normal message response
            try:
                data = sock.recv(BUFFER_SIZE)
            except ConnectionResetError:
                print("[!] Connection reset by server.")
                break

            if not data:
                print("[*] Server closed the connection.")
                break

            print(f"Server: {data.decode(ENCODING).strip()}")

    except KeyboardInterrupt:
        print("\n[!] Client interrupted by user (Ctrl+C).")


def run_client(host: str = HOST, port: int = PORT) -> None:
    """
    High-level client runner: create socket, connect, run loop, clean up.
    """
    sock = create_client_socket()
    try:
        if not connect_to_server(sock, host, port):
            return  # connection failed, finally will close the socket

        client_message_loop(sock)
    finally:
        try:
            sock.close()
        except OSError:
            pass
    
    print("[*] Client socket closed. Client shut down cleanly.")


if __name__ == "__main__":
    run_client()
