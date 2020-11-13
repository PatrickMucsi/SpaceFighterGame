import socket
import threading
import pickle
import multiprocessing as mp
from NetworkMessage import NetworkMessage

class Client:
    def __init__(self):
        self.HEADER = 2048 * 4
        self.PORT = 5050
        self.SERVER = '47.42.150.73'# input("input ip: ")
        self.DISCONNECT_MESSAGE = '!DISCONNECT'
        self.ADDR = (self.SERVER, self.PORT)

        self.client = None
        self.connected = False

    def connect(self):
        print(f'connecting to {self.SERVER}...')
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
        self.connected = True
        # self.network_connection = threading.Thread(target=self.get_updates, args=())
        # self.connected = True
        # self.network_connection.start()

    def disconnect(self, id):
        print('disconnecting from server')
        message = self.create_message('cmd', {'server': {'id': id, 'command':self.DISCONNECT_MESSAGE}})
        self.connected = False
        self.send(message)

    def send(self, message):
        self.client.send(self.encode_message(message))
        return self.decode_message(self.client.recv(self.HEADER)) if self.connected else None

    def create_message(self, message_type, message):
        return NetworkMessage(message_type, message)

    def encode_message(self, message):
        return pickle.dumps(message)

    def decode_message(self, message):
        return pickle.loads(message)
