
class ServerClient:

    def __init__(self, name, conn):
        self.name = name
        self.conn = conn
        self.is_connected = True
        self.connected = False


