import socket

def socket_example_client():
    host = '127.0.0.1'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        message = "Hello, Server!"
        client_socket.sendall(message.encode('utf-8'))

        data = client_socket.recv(1024)
        print(f"Received from server: {data.decode('utf-8')}")
