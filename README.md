# CYB333 Socket Connection Project

A TCP client-server communication system demonstrating socket programming fundamentals in Python.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)

## Overview

This project implements a simple TCP-based client-server architecture using Python's built-in `socket` module. It showcases proper socket initialization, connection lifecycle management, bidirectional message exchange, comprehensive error handling, and graceful shutdown procedures.

## Features

### Server
- **Multi-command support** - Interactive command processing system
- **Real-time information** - Time and uptime queries
- **Message echo** - Echo back any text messages from clients
- **Connection management** - Single client connection with proper lifecycle handling
- **Error handling** - Comprehensive exception handling for network errors
- **Graceful shutdown** - Clean resource cleanup on exit

### Client
- **Interactive interface** - Simple command-line interface for user input
- **Auto-reconnect handling** - Clear error messages for connection issues
- **Welcome screen** - Displays available commands on connection
- **Timeout management** - Connection timeout for unresponsive servers
- **Clean disconnection** - Proper socket closure and resource cleanup

### Available Commands
| Command | Description |
|---------|-------------|
| `time` | Get the current server time |
| `uptime` | Get server uptime (hours, minutes, seconds) |
| `help` | Display all available commands |
| `exit` | Disconnect from the server |
| Any text | Echo the message back from server |

## Requirements

- **Python**: 3.11
- **Dependencies**: None (uses Python standard library only)
- **OS**: Linux, macOS, Windows (any OS with Python 3.11)

### Python Modules Used
- `socket` - Network communication
- `sys` - System-specific parameters
- `time` - Time tracking for uptime
- `datetime` - Timestamp formatting

## Installation

### Option 1: Using Conda (Recommended)

```bash
# Create a new conda environment with Python 3.11
conda create -n CYB333_socket_connection python=3.11

# Activate the environment
conda activate CYB333_socket_connection

# Verify Python version
python --version  # Should output: Python 3.11.x
```

### Option 2: Using venv

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate the environment
source venv/bin/activate  # On Linux/macOS
# OR
venv\Scripts\activate  # On Windows

# Verify Python version
python --version
```

### Clone the Repository

```bash
git clone https://github.com/phlypinoy/CYB333_socket_connection.git
cd CYB333_socket_connection
```

## Usage

### Starting the Server

Open a terminal and run:

```bash
python server.py
```

Expected output:
```
[+] Server listening on 127.0.0.1:5000 ...
```

### Starting the Client

Open a **separate terminal** and run:

```bash
python client.py
```
