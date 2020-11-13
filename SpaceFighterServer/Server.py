import socket
import pickle
import threading
import multiprocessing as mp
from NetworkMessage import NetworkMessage

class Server:
    def __init__(self):
        self.HEADER = 2048 * 4
        self.PORT = 5050
        self.SERVER = '47.42.150.73'#socket.gethostbyname(socket.gethostname())
        self.network = None
        self.ADDR = (self.SERVER, self.PORT)
        self.DISCONNECT_MESSAGE = '!DISCONNECT'
        self.create_server()

    def create_server(self):
        print(f'Starting server on {self.SERVER}:{self.PORT}')
        self.network = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.network.bind(self.ADDR)
        self.network.listen()

    def create_message(self, type, message):
        return NetworkMessage(type, message)
