import socket
import threading
import queue
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up global variables
SERVER_IP = '192.168.41.75'  # Replace with the actual IP address of the server
SERVER_PORT = 9000  # Replace with the desired port

# Create a queue to store the messages
message_queue = queue.Queue()

# Simple authentication mechanism
# Replace with a proper authentication mechanism in production
users = {
    'user1': 'password1',
    'user2': 'password2',
}

def handle_client(client_socket, addr):
    try:
        # Authenticate the user
        while True:
            data = client_socket.recv(1024)
            if not data:
                logging.debug(f"Connection closed by client {addr}")
                break

            # Decode the data and check if it is a valid user
            message = json.loads(data.decode())
            if message['type'] == 'auth':
                username = message['data']['username']
                password = message['data']['password']
                if username in users and users[username] == password:
                    logging.debug(f"User {username} authenticated")
                    client_socket.send(json.dumps({'type': 'auth', 'data': {'success': True}}).encode())
                    break
                else:
                    logging.debug(f"User {username} authentication failed")
                    client_socket.send(json.dumps({'type': 'auth', 'data': {'success': False}}).encode())
            else:
                logging.debug(f"User {addr} sent invalid message during authentication")
                client_socket.send(json.dumps({'type': 'auth', 'data': {'success': False}}).encode())

        # Start the message handling loop
        def receive_message():
            while True:
                data = client_socket.recv(1024)
                if not data:
                    logging.debug(f"Connection closed by client {addr}")
                    break

                # Decode the data and put it in the queue
                message = json.loads(data.decode())
                if message['type'] == 'message':
                    logging.info(f"Received message from {addr}: {message['data']}")
                    message_queue.put(message['data'])
                    logging.debug(f"Message added to queue: {message['data']}. Queue size: {message_queue.qsize()}")

        def send_message():
            while True:
                # Wait for a message to be put in the queue
                #data = message_queue.get()
                data = input("Enter message: ")
                client_socket.send(json.dumps({'type': 'message', 'data': data}).encode())

        # Start the threads
        threading.Thread(target=receive_message).start()
        threading.Thread(target=send_message).start()

    except Exception as e:
        logging.error(f"Error handling connection from {addr}: {e}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))
server.listen(5)

logging.info(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

while True:
    try:
        client_socket, addr = server.accept()
        logging.info(f"Connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()
    except Exception as e:
        logging.error(f"Error accepting connection: {e}")
