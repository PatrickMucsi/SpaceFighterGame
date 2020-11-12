from Client import Client
import uuid

class SpaceFighterClient:
    def __init__(self, username):
        self.client = Client()
        self.username = username
        self.id = uuid.uuid4()
        self.connect()

    def connect(self):
        self.client.connect()
        print('connecting to server...')

    def update_server(self, player):
        return self.send_message('pos', player)

    def disconnect(self):
        self.client.disconnect(self.id)

    def send_message(self, type, message):
        message = self.client.create_message(type, message)
        return self.client.send(message)
