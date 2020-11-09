import socket
import time
import threading
import pickle
import multiprocessing as mp

class NetworkMessage:
    def __init__(self, type, message):
        self.type = type
        self.message = message
        self.network_message = {'type': self.type, 'info': self.message}


class Client:
    def __init__(self, game_queue):
        self.HEADER = 2048
        self.PORT = 5050
        self.SERVER = '47.42.150.73'#'192.168.56.1'
        self.DISCONNECT_MESSAGE = '!DISCONNECT'
        self.ADDR = (self.SERVER, self.PORT)
        self.id = None

        self.network_queue = game_queue
        self.client = None
        self.network_connection = None
        self.connected = False

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
        print('connecting to server...')
        self.network_connection = threading.Thread(target=self.get_updates, args=(self.network_queue, ))
        self.connected = True
        self.network_connection.start()

    def disconnect(self):
        print('disconnecting from server')
        self.send(self.create_message('cmd', 'disconnect'))
        self.connected = False
        self.network_connection.join()

    def send(self, message):
        self.client.send(self.encode_message(message))

    def create_message(self, message_type, message):
        return NetworkMessage(message_type, message)

    def encode_message(self, message):
        return pickle.dumps(message.network_message)

    def decode_message(self, message):
        return pickle.loads(message)

    def get_updates(self, network_queue):
        self.connected = True
        while self.connected:
            encoded_message = self.client.recv(self.HEADER)
            if encoded_message != b'':
                decoded_message = self.decode_message(encoded_message)
                if decoded_message.get('id') != None:
                    self.id = decoded_message.get('id')
                else:
                    network_queue.put(decoded_message)
                    decoded_message = self.decode_message(encoded_message)
