import socket
import threading


server_ip = '192.168.41.75'
server_port = 5001


def handle_client(client_socket, addr):
    try:
        def receive():
            while True:
                data = client_socket.recv(1024)
                if not data:
                    print("Connection closed by client")
                    break
                print(f"Received from {addr}: {data.decode()}")

        def send():
            while True:
                data = input("Enter message: ")
                client_socket.send(data.encode()) 

        threading.Thread(target=receive).start()
        threading.Thread(target=send).start()

    except Exception as e:
        print(f"Error handling from {addr}: {e}")               

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, server_port))
server.listen(5)

print(f"Server listening on {server_ip}:{server_port}")

while True:
    try:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()
    except Exception as e:
        print(f"Error: {e}")