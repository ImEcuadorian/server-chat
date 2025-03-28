import socket
import threading

class Client:

    def __init__(self, ip_server, port_server):
        self.ipServer = ip_server
        self.portServer = port_server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.client_socket.connect((self.ipServer, self.portServer))
            print(f"Connected to server at {self.ipServer}:{self.portServer}")
        except socket.error as e:
            print(f"Error connecting to server: {e}")
            return None
        return self.client_socket

    def send_message(self, message):
        try:
            self.client_socket.sendall(message.encode())
            print(f"Sent data: {message}")
        except socket.error as e:
            print(f"Error sending data: {e}")
            self.client_socket.close()

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                print(f"Received: {data.decode()}")
            except socket.error as e:
                print(f"Error receiving data: {e}")
                break

    def start(self):
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

if __name__ == "__main__":
    client = Client("172.17.42.153", 80)
    client.connect()
    client.start()
    while True:
        message = input("Enter message: ")
        if message.lower() == "exit":
            break
        client.send_message(message)
    client.client_socket.close()