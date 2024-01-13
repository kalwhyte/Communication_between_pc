import socket
import json
import threading

server_ip = '192.168.41.75'
server_port = 6000

def handle_server(server_socket):
    try:
        def receive():
            while True:
                data = server_socket.recv(1024)
                if not data:
                    print("Connection closed by server")
                    break
                message = json.loads(data.decode())
                print(f"Received from server: {message['data']}")

        def send():
            while True:
                data = input("Enter message: ")
                server_socket.send(json.dumps({'type': 'message', 'data': data}).encode())

        threading.Thread(target=receive).start()
        threading.Thread(target=send).start()

    except Exception as e:
        print(f"Error: {e}")

# Connect to the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((server_ip, server_port))

# Authenticate
username = input("Enter username: ")
password = input("Enter password: ")
server_socket.send(json.dumps({'type': 'auth', 'data': {'username': username, 'password': password}}).encode())

# Handle the server
handle_server(server_socket)