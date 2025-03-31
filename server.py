import socket
import threading

from serverclient import ServerClient

def receive_data(conn):
    try:
        data = conn.recv(1024).decode().strip()
        return data if data else None
    except socket.error:
        return None


def send_data(conn, message):
    try:
        conn.sendall((message + "\n").encode())
    except socket.error:
        pass


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        try:
            self.server_socket.bind((self.ip, self.port))
            self.server_socket.listen(5)
            print(f"Server listening on {self.ip}:{self.port}")
        except socket.error as e:
            print(f"Error binding server: {e}")
            return

        while True:
            conn, addr = self.server_socket.accept()
            print(f"New connection from {addr}")

            send_data(conn, "Welcome to the chat server!\nEnter your name: ")
            name = receive_data(conn).strip()

            if not name:
                conn.close()
                continue

            client = ServerClient(name, conn, addr)
            self.clients.append(client)
            print(f"{name} has joined the chat.")
            self.broadcast(f"{name} has joined the chat.", client)

            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, client):
        while True:
            message = receive_data(client.conn)
            if message is None or message.lower() == "exit":
                print(f"{client.name} has left the chat.")
                self.broadcast(f"{client.name} has left the chat.", client)
                self.clients.remove(client)
                client.conn.close()
                break

            self.broadcast(f"{client.name}: {message}", client)

    def broadcast(self, message, sender_client):
        for client in self.clients:
            if client != sender_client:
                send_data(client.conn, message)


if __name__ == "__main__":
    server = Server("172.17.42.153", 8080)
    server.start()
