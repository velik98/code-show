import socket
import os
import sys


def send_file(connection, filename):
    file_size = os.path.getsize(filename)
    sent_bytes = 0

    with open(filename, "rb") as file:
        for data in file:
            connection.sendall(data)
            sent_bytes += len(data)
            completion = (sent_bytes / file_size) * 100
            sys.stdout.write(f"\rTransmitting: {completion:.2f}%")
            sys.stdout.flush()

    sys.stdout.write("\n")
    sys.stdout.flush()


def connect_to_server(host, port, filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    client_socket.send(filename.encode())
    filename_sent = client_socket.recv(1024).decode()
    print(f"Sending file: {filename}")
    print(f"Server received: {filename_sent}")

    send_file(client_socket, filename)
    print("File sent successfully")

    client_socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <server_address> <server_port> <input_file>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    input_file = sys.argv[3]

    if not os.path.isfile(input_file):
        print(f"Input file '{input_file}' does not exist")
        sys.exit(1)

    with open(input_file, "r") as file:
        filenames = file.read().splitlines()

    for filename in filenames:
        connect_to_server(host, port, filename)
