import socket
import threading

class Client:
    def __init__(self, ip_server, port_server):
        self.ip_server = ip_server
        self.port_server = port_server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False  # Flag para verificar si está conectado

    def connect(self):
        """Intenta conectar con el servidor."""
        try:
            self.client_socket.connect((self.ip_server, self.port_server))
            print(f"✅ Connected to server at {self.ip_server}:{self.port_server}")
            self.connected = True
        except socket.error as e:
            print(f"❌ Error connecting to server: {e}")
            self.client_socket.close()
            self.connected = False  # Evita enviar datos si no hay conexión

    def send_message(self, message):
        """Envía un mensaje al servidor si está conectado."""
        if not self.connected:
            print("⚠️ Not connected to the server.")
            return
        try:
            self.client_socket.sendall(message.encode())
        except socket.error as e:
            print(f"❌ Error sending data: {e}")
            self.client_socket.close()
            self.connected = False  # Evita más envíos tras una desconexión

    def receive_messages(self):
        """Escucha mensajes del servidor en un hilo separado."""
        while self.connected:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    print("🔌 Disconnected from server.")
                    self.connected = False
                    break
                print(f"\n📩 {data.decode()}")
            except socket.error as e:
                print(f"❌ Error receiving data: {e}")
                self.connected = False
                break
        self.client_socket.close()

    def start(self):
        """Inicia el cliente y el hilo de recepción de mensajes."""
        self.connect()
        if self.connected:
            receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            receive_thread.start()

            while True:
                message = input("💬 Enter message (or 'exit' to quit): ")
                if message.lower() == "exit":
                    print("🔌 Disconnecting...")
                    break
                self.send_message(message)

            self.client_socket.close()

if __name__ == "__main__":
    client = Client("127.0.0.1", 8080)  # Asegúrate de que el servidor esté en esta IP/puerto
    client.start()
