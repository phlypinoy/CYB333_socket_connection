# AI Coding Agent Instructions for CYB333 Socket Connection

## Project Overview

This is a **TCP client-server communication system** written in Python for CYB333 coursework. It demonstrates clean socket programming patterns: proper initialization, connection lifecycle management, error handling, and graceful shutdown.

**Key Architecture:**
- **Server** (`server.py`): Listens on `127.0.0.1:5000`, accepts single client, receives/responds to messages
- **Client** (`client.py`): Connects to server, reads user input, sends messages, receives responses
- **Data Flow**: User input → Client socket → Network → Server socket → Response echoed back

## Environment & Running

**Python Version**: 3.11 (required, specified in README)

**Setup**:
```bash
conda create -n CYB333_socket_connection.conda python=3.11
conda activate CYB333_socket_connection.conda
```

**Running** (in separate terminals):
```bash
# Terminal 1: Start server
python server.py

# Terminal 2: Start client
python client.py
```

Both programs use only Python standard library (`socket`, `sys`) — no external dependencies.

## Code Patterns & Conventions

### Socket Initialization
- **Constants at module level**: `HOST`, `PORT`, `BUFFER_SIZE`, `ENCODING` make configuration explicit and easy to modify
- **Context managers** (`with socket.socket(...)`): Ensures automatic cleanup; preferred pattern throughout
- **SO_REUSEADDR**: Used in server to avoid "Address already in use" after restart

### Connection Handling
- **Server**: Blocks on `accept()`, handles one client at a time
- **Client**: Uses `settimeout(CONNECT_TIMEOUT)` (5 seconds) to prevent indefinite hangs
- Both use `conn.recv()` which returns empty bytes (`b''`) when connection closes — standard way to detect disconnection

### Message Exchange
- All messages are **UTF-8 encoded** with newline delimiters: `(message + "\n").encode(ENCODING)`
- **Exit protocol**: Client sends "exit" → Server responds with goodbye → Both close cleanly
- Server echoes pattern: `f"Server received: {message}"`

### Error Handling Patterns
Both files handle these socket-specific exceptions:
- `ConnectionRefusedError`: Server not running or wrong port
- `ConnectionResetError`: Abrupt client/server disconnect
- `BrokenPipeError`: Send fails because peer closed connection
- `socket.timeout`: Connect attempt exceeded timeout threshold
- `OSError`: Generic socket errors (bind failures, etc.)

All exception messages use `[!]` prefix; status messages use `[+]`, `[*]`, `[<]`, `[>]` for clarity.

### Shutdown Patterns
- **KeyboardInterrupt** (`Ctrl+C`): Caught at top level, prints message, exits cleanly
- **EOF** (client only, `Ctrl+D`): Treated as user close request
- **graceful socket close**: Always in `finally` block or context manager to prevent resource leaks
- Print `"[*] ... shut down cleanly."` before exit to confirm orderly termination

## Key Functions & Their Contracts

**Server**:
- `start_server()`: Main function; no parameters, returns on clean shutdown

**Client**:
- `create_client_socket()` → `socket.socket`: Returns initialized socket with timeout
- `connect_to_server(sock, host, port)` → `bool`: True if connected, False if failed
- `client_message_loop(sock)`: Main interaction loop; reads input, sends/receives
- `run_client(host=HOST, port=PORT)`: High-level runner; handles connection and cleanup

## When Making Changes

1. **Modify message protocol** (e.g., add request/response formats): Update both `ENCODING` and decoding logic in both files
2. **Change port or host**: Update module-level constants; both use same values
3. **Add features** (e.g., multiple clients): Server architecture currently handles one client; would require threading/async refactor
4. **Error handling**: Follow existing `[!]` log prefix and exception pattern; don't swallow exceptions silently
5. **Testing**: Manual two-terminal test is standard; run server first, then client, type messages including "exit"

## Dependencies & Constraints

- **Python 3.11 only** (per README)
- **Localhost only**: `127.0.0.1` hardcoded; this is intentional for security/testing
- **Single client**: Server accepts and serves one client at a time
- **No external packages**: Only `socket` and `sys` from stdlib

## Important Implementation Details

- **recv() behavior**: Receiving 0 bytes means graceful disconnect, not error; handle immediately
- **Newline handling**: Messages include `\n` on wire but `.strip()` on receive to remove it before printing
- **Timeouts**: Only client uses timeout; server blocks indefinitely on accept (acceptable for single-client design)
- **Empty input**: Client skips empty lines before sending (intentional filtering)
