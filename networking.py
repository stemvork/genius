import socket

packet_size = 2048
packet_count = 2


class Network:
    def __init__(self, addr=None):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server = "192.168.0.101"  # personal
        if not addr:
            self.server = "192.168.0.103"  # school
        else:
            self.server = addr
        self.port = 5555
        self.addr = (self.server, self.port)
        # Try to connect, receive player_id
        self.player_id = self.connect()

    def get_player_id(self):
        return self.player_id

    # Upon connecting, return player_id
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    # Abbreviation for sending data
    def send(self, data):
        try:
            # Send the encoded request string / data
            self.client.send(str.encode(data))

            # Receive server response
            response = self.client.recv(packet_size * packet_count).decode()
            return response
        except socket.error as e:
            print(e)
