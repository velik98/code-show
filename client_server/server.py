import argparse
import os
import socket


def receive_file(connection, file):
    if os.path.exists(file):
        base, ext = os.path.splitext(file)
        i = 1
        while os.path.exists(f"{base}({i}){ext}"):
            i += 1
        file = f"{base}({i}){ext}"

    with open(file, "wb") as storage:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            storage.write(data)


def start_server(host, port, w_dir):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    while True:
        connection, address = server_socket.accept()
        print(f"Connected to client: {address}")
        file = connection.recv(1024).decode()
        connection.send(file.encode())
        print(file)
        path = os.path.join(w_dir, file)
        print(f"Receiving file: {file}")
        receive_file(connection, path)127
        print(f"saved as: {path}")
        connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="server configuration")
    parser.add_argument("--ip", default="127.0.0.1", help="IP address to connect the server to")
    parser.add_argument("--port", default=1234, help="Port number")
    parser.add_argument("--work-dir", default= os.getcwd(), help="Working directory")
    args = parser.parse_args()
    start_server(args.ip, args.port, args.work_dir)
