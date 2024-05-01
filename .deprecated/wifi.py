import socket

# Set up socket
server_ip = '0.0.0.0'  # Listen on all interfaces
server_port = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(1)

print("Waiting for connection...")

while True:
    client_socket, client_address = server_socket.accept()
    print("Connection from:", client_address)

    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                print("Connection closed by client")
                break
            print("Received message:", data)
        except Exception as e:
            print("Error:", e)
            break

    client_socket.close()
