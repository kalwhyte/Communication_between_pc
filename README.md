# Multithreaded TCP Server

This is a simple multithreaded TCP server implemented in Python. It uses the built-in `socket` and `threading` modules to handle multiple client connections simultaneously.

## How it works

When a client connects, the server starts two threads: one for receiving data from the client and one for sending data to the client. This allows the server to send and receive data simultaneously.

The server listens for connections on IP address `192.168.41.75` and port `5001`.

## Running the server

To run the server, simply execute the script using Python 3:

```bash
python3 man.py