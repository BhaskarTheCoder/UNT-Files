import socket

def socket_example_server():
    host = '127.0.0.1'
    port = 65432

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    print(f"Server started at {host}:{port}")

    server_socket.listen(5)
    print("Waiting for a connection...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Received: {data.decode('utf-8')}")
                conn.sendall(data)
