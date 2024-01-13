"""import socket
import threading

# Server IP and port
server_ip = '192.168.41.75'
server_port = 5000


def handle_client(client_socket, client_address):
    print(f"Connection from {client_address}")

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print(f"Client {client_address} disconnected")
                break
            print(f"Received from {client_address}: {data.decode()}")
    
            client_socket.send(data)

    except Exception as e:
        print(f"Error handling connection from {client_address}: {e}")

    finally:
        client_socket.close()
        print(f"Connection from {client_address} closed")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, server_port))
server.listen(5)

print(f"Listening on {server_ip}:{server_port}")

try:
    while True:
        client_socket, client_address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

except KeyboardInterrupt:
    print('Interrupted')

# Close the socket
finally:
    server.close()"""
'''
import socket
import threading
import logging
import time

logging.basicConfig(level=logging.INFO)

# Server IP and port
server_ip = '192.168.41.75'
server_port = 5000

def receive_data(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            logging.info(f"Server closed connection")
            break
        logging.info(f"Received from server: {data.decode()}")

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
except Exception as e:
    logging.error(f"Connection to {server_ip}:{server_port} failed: {e}")
    exit(1)

logging.info(f"Connected to {server_ip}:{server_port}")


# Start a thread to receive data from the server
receive_thread = threading.Thread(target=receive_data, args=(client,))
receive_thread.start()

# Send data
while True:
    time.sleep(0.1)
    data = input("Enter data to send (or 'exit' to stop): ")
    if data.lower() == 'exit':
        break
    client.send(data.encode())'''


import socket
import threading

'''
def send_data(server_ip, server_port, message):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server_ip, server_port))

        response = client.recv(1024)
        print(f"Received from server: {response.decode()}")

    except KeyboardInterrupt:
        print('Interrupted')

    except Exception as e:
        print(f"Connection to {server_ip}:{server_port} failed: {e}")
    
    finally:
        client.close()


if __name__ == '__main__':
    server_ip = '192.168.41.75'
    server_port = 5110

    message = input("Enter data to send (or 'exit' to stop): ")

    send_data(server_ip, server_port, message)'''


def handle_server(server_socket):
    def receive_data(client_socket):
        while True:
            data = client_socket.recv(1024)
            if not data:
                print(f"Server closed connection")
                break
            print(f"Received from server: {data.decode()}")

    def send_data(client_socket):
        while True:
            data = input("Enter data to send (or 'exit' to stop): ")
            if data.lower() == 'exit':
                break
            client_socket.send(data.encode())

    receive_thread = threading.Thread(target=receive_data, args=(server_socket,))
    send_thread = threading.Thread(target=send_data, args=(server_socket,))

    receive_thread.start()
    send_thread.start()

    receive_thread.join()
    send_thread.join()

try:
    server_ip = '192.168.41.75'
    server_port = 5001
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    handle_server(client)
except KeyboardInterrupt:
    print(f"Connection to {server_ip}:{server_port} failed: {e}")
finally:
    client.close()