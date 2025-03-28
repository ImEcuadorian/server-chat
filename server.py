import socket
import threading

from serverclient import ServerClient


class Server:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.clients = []

    def connect(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server_socket.bind((self.ip, self.port))
            print(f"Server listening on {self.ip}:{self.port}")
        except socket.error as e:
            print(f"Error binding server: {e}")
            return None

        server_socket.listen(5)
        while True:
            connection, addr = server_socket.accept()
            print(f"Connection from {addr}")
            self.send_data(connection, "Welcome to the server!")
            self.send_data(connection, "Type 'exit' to disconnect.")
            self.send_data(connection, "Type your name:")
            name = self.receive_data(connection).decode()
            client = ServerClient(name, connection)
            self.clients.append(client)
            client_thread = threading.Thread(target=self.handle_client, args=(connection,))
            client_thread.start()

    def handle_client(self, client):
        while True:
            data = self.receive_data(client.conn)
            if data is None or data.decode() == "exit":
                self.clients.remove(client)
                break
            self.broadcast(f"{client.name}: {data.decode()}", client)
        client.conn.close()

    def broadcast(self, message, sender_client):
        for client in self.clients:
            if client != sender_client:
                self.send_data(client.conn, message)

    def receive_data(self, conn):
        try:
            return conn.recv(1024)
        except socket.error as e:
            conn.close()
            return None

    def send_data(self, conn, data):
        try:
            conn.sendall(data)
        except socket.error as e:
            conn.close()


if __name__ == "__main__":
    server = Server("172.17.42.153", 80)
    server.connect()
