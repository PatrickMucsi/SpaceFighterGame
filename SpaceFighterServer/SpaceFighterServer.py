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
            if operation == 'dir':
                direction = message.get('msg').get('info')
                self.player_one.move(direction)
        if message.get('user') == 1:
            operation = message.get('msg').get('type')
            if operation == 'dir':
                direction = message.get('msg').get('info')
                self.player_two.move(direction)

    def update_clients(self):
        if self.player_one.has_moved or self.player_two.has_moved:
            message = {'p1': self.server.encode_message({'x': self.player_one.x, 'y': self.player_one.y}),
                    'p2': self.server.encode_message({'x': self.player_two.x, 'y': self.player_two.y})}
            encoded_message = self.server.encode_message(message)
            self.server.update(message)
            self.player_one.has_moved = False
            self.player_two.has_moved = False
        # if self.player_two.has_moved:
        #     message = self.server.encode_message('player two moved')
        #     self.server.update(message)
        #     self.player_two.has_moved = False


    # def update_clients(self):
    #     while self.server.total_connections == 2:
    #         self.send_player_positions()
    #         if not self.message_queue.empty():
    #             print('operation detected')
    #             operation = self.message_queue.get()
    #             if operation.get('user') == 1:
    #                 print('player one moved')
    #                 print(operation.get('msg'))
    #                 # if operation.get('dir') == 'l':
    #                 #     self.player_one.x -= 4
    #                 # if operation.get('dir') == 'r':
    #                 #     self.player_one.x += 4
    #                 #self.player_one.move(self.server.decode_message(operation.get('msg').get('info')))
    #             if operation.get('user') == 2:
    #                 print('player two moved')
    #                 self.player_two.move(self.server.decode_message(operation.get('msg').get('info')))

    # def send_player_positions(self):
    #     message = {'msg' : {
    #         'type': 'pos',
    #         'p1': pickle.dumps(self.player_one.get_position()),
    #         'p2': pickle.dumps(self.player_two.get_position())
    #     }}
    #     self.server.send(self.server.encode_message(message))
    #     player_one_pos = NetworkMessage(1, 'pos', self.player_one.get_position())
    #     player_two_pos = NetworkMessage(1, 'pos', self.player_two.get_position())



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
        self.starting_lives = 3
        self.movement_speed = 4

    def move(self, direction):
        print(f'ship moved {direction}')
        self.has_moved = True
        if direction == 'left':
            self.x -= self.movement_speed
        if direction == 'right':
            self.x += self.movement_speed
    # def move(self, position):
    #     self.x = position.get('x')
    #     self.y = position.get('y')

    def get_position(self):
        return {'x': self.x, 'y': self.y}

s = SpaceFighterServer()
