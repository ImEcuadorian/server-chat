
class ServerClient:
    def __init__(self, name, conn, address):
        self.name = name
        self.conn = conn
        self.address = address
        self.is_connected = True


