from Server import Server
import threading
import multiprocessing as mp
import pickle

class SpaceFighterServer:
    def __init__(self):
        self.message_queue = mp.Queue()
        self.server = Server(self.message_queue)
        self.server.wait_for_connection()
        self.server.wait_for_connection()
        self.player_one = ServerShip(300, 650, 50, 50)
        self.player_two = ServerShip(300, 650, 50, 50)
        self.start()

    def start(self):
        lobby = threading.Thread(target=self.create_lobby, args=(self.message_queue, ))
        lobby.start()

    def create_lobby(self, message_queue):
        while self.server.total_connections == 2:
            self.update_clients()
            if not message_queue.empty():
                message = message_queue.get()
                self.handle_message(message)

    def handle_message(self, message):
        if message.get('user') == 0:
            operation = message.get('msg').get('type')
            if operation == 'move':
                print(f'user: 0\nmessage: {message}\noperation: {operation}')
                direction = message.get('msg').get('info')
                #location = self.server.decode_message(encoded_location)
                self.player_one.move(direction)
        if message.get('user') == 1:
            operation = message.get('msg').get('type')
            if operation == 'move':
                print(f'user: 1\nmessage: {message}\noperation: {operation}')
                direction = message.get('msg').get('info')
                self.player_two.move(direction)

    def update_clients(self):
        if self.player_one.has_moved or self.player_two.has_moved:
            message = {'type': 'pos', 'info': {'p1': self.server.encode_message({'x': self.player_one.x, 'y': self.player_one.y}),
                                            'p2': self.server.encode_message({'x': self.player_two.x, 'y': self.player_two.y})}}
            encoded_message = self.server.encode_message(message)
            self.server.update(message)
            self.player_one.has_moved = False
            self.player_two.has_moved = False


class NetworkMessage:
    def __init__(self, user, type, message):
        self.type = type
        self.message = message
        self.info = self.server.encode_message(message) if self.type == 'pos' else self.message
        self.msg = {'msg': {
            'user': user,
            'type': self.type,
            'info': self.info,
        }}

class ServerShip:
    def __init__(self, x, y, width, height):
        self.has_moved = False
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.starting_lives = 3
        self.movement_speed = 6

    def move(self, direction):
        self.has_moved = True
        if direction == 'left':
            next_location = self.x - self.movement_speed
            if next_location > 0:
                self.x -= self.movement_speed
        elif direction == 'right':
            next_location = self.x + self.movement_speed
            if next_location < 750 - self.width:
                self.x += self.movement_speed

    def get_position(self):
        return {'x': self.x, 'y': self.y}

s = SpaceFighterServer()
