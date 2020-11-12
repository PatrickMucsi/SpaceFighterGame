from Server import Server
from Ship import Ship
import socket
import pickle
import threading
import multiprocessing as mp
import random
import sys

class SpaceFighterServer:
    def __init__(self):
        random.seed()
        self.server = Server() #eventually Server(<ip address>, <port>, <total players?>)
        self.total_connections = 0
        self.players = []

    def start(self, total_players):
        while self.total_connections < total_players:
            self.wait_for_connection()

    def wait_for_connection(self):
        print('waiting for player...')
        conn, addr = self.server.network.accept()
        id = self.total_connections
        thread = threading.Thread(target=self.handle_connection, args=(conn, addr, id))
        self.total_connections += 1
        thread.start()

    def handle_connection(self, conn, addr, user_id):
        print(f'{addr[0]} connected to the server')
        connected = True
        while connected:
            encoded_message = conn.recv(self.server.HEADER)
            if encoded_message != b'':
                decoded_message = self.decode_message(encoded_message)
                return_message = None
                if decoded_message.type == 'cmd':
                    if 'server' in decoded_message.message:
                        command_info = decoded_message.message.get('server')
                        if command_info.get('command') == self.server.DISCONNECT_MESSAGE:
                            self.remove_player_with_id(command_info.get('id'))
                            connected = False
                            self.total_connections -= 1
                    else:
                        return_message = self.handle_command(decoded_message)
                if decoded_message.type == 'pos':
                    return_message = self.handle_movement(decoded_message)

                if return_message != None:
                    conn.sendall(self.encode_message(return_message))

        conn.close()

    def handle_movement(self, message):
        new_player = message.message
        old_player = self.get_player_with_id(new_player.id)
        self.players.remove(old_player)
        self.players.append(new_player)
        return self.server.create_message('positions', self.players)

    def handle_command(self, message):
        command = message.message
        if 'server' in command:
            command_info = command.get('server')
            if command_info.get('command') == self.server.DISCONNECT_MESSAGE:
                self.remove_player_with_id(command_info.get('id'))
                connected = False
                self.total_connections -= 1
        if 'start' in command:
            start_info = command.get('start')
            username = start_info.get('username')
            id = start_info.get('id')
            x = y = random.randrange(50, 700)
            new_player = Ship(username, id, (x, y), (50, 50), 'basic')
            self.players.append(new_player)
            print('There are now {} players'.format(len(self.players)))
            return self.server.create_message('start', new_player)
        else:
            return None

    def remove_player_with_id(self, id):
        for player in self.players:
            if player.id == id:
                self.players.remove(player)

    def get_player_with_id(self, id):
        for player in self.players:
            if player.id == id:
                return player


    def update(self, message):
        self.send(self.encode_message(message))

    def send(self, message):
        for conn in self.connections:
            conn.send(message)

    def decode_message(self, message):
        return pickle.loads(message)

    def encode_message(self, message):
        return pickle.dumps(message)
