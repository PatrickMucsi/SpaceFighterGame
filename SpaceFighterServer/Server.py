import socket
import pickle
import threading

class Server:
    def __init__(self, shared_queue):
        self.HEADER = 2048
        self.PORT = 5050
        self.SERVER = '192.168.1.18'#socket.gethostbyname(socket.gethostname())
        self.server_connection = None
        self.ADDR = (self.SERVER, self.PORT)
        self.DISCONNECT_MESSAGE = '!DISCONNECT'
        self.create_server_connection()

        self.connections = []
        self.total_connections = 0
        self.message_queue = shared_queue

    def wait_for_connection(self):
        print('waiting for player...')
        conn, addr = self.server_connection.accept()
        id = self.total_connections
        thread = threading.Thread(target=self.handle_connection, args=(conn, addr, id, self.message_queue, ))
        #thread = mp.Process(target=self.handle_connection, args=(conn, addr, user_id))
        self.total_connections += 1
        thread.start()

    def handle_connection(self, conn, addr, user_id, message_queue):
        print(f'{addr[0]} connected to the server')
        connected = True
        self.connections.append(conn)
        conn.send(self.encode_message({'id': user_id}))
        while connected:
            encoded_message = conn.recv(self.HEADER)
            decoded_message = self.decode_message(encoded_message)
            if decoded_message.get('type') == 'cmd':
                if decoded_message.get('info') == 'disconnect':
                    connected = False
                    self.total_connections -= 1
            else:
                message = {'user': user_id, 'msg': decoded_message}
                #print(f'putting [{message}] into queue')
                message_queue.put({'user': user_id, 'msg': decoded_message})


        self.connections.remove(conn)
        conn.close()
        message_queue.put(f'{addr[0]} disconnected')

    def update(self, message):
        self.send(self.encode_message(message))

    def send(self, message):
        for conn in self.connections:
            conn.send(message)

    def decode_message(self, message):
        return pickle.loads(message)

    def encode_message(self, message):
        return pickle.dumps(message)

    def create_server_connection(self):
        print(f'Starting server on {self.SERVER}:{self.PORT}')
        self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_connection.bind(self.ADDR)
        self.server_connection.listen()
