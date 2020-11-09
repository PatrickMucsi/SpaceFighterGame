import pygame
import os, time, random, sys
import multiprocessing as mp

from Client import Client
from SpaceFighterPlayerHandler import SpaceFighterPlayerHandler as SFPlayerHandler

class SpaceFighterCore:
    def __init__(self):
        pygame.init()
        self.WIDTH = 750
        self.HEIGHT = 750
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Space Fighter v0.4')

        self.movement_queue = mp.Queue()
        self.player_handler = SFPlayerHandler(self.movement_queue)

        self.client = Client(self.movement_queue)
        self.client.connect()

    def run(self):
        print('Starting game')
        running = True
        FPS = 60
        clock = pygame.time.Clock()

        def redraw_window():
            self.WIN.fill((0,0,0))

            self.player_handler.render(self.WIN)

            pygame.display.update()

        def update():
            if not self.movement_queue.empty():
                message = self.movement_queue.get()
                if message.get('type') == 'pos':
                    self.player_handler.process_network_message(self.client, message.get('info'))
                if message.get('type') == 'attack':
                    pass

        while running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.client.disconnect()
                    running = False
                    sys.exit()

            update()
            redraw_window()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]: #left
                client_message = self.client.create_message('move', 'left')
                self.client.send(client_message)
            if keys[pygame.K_d]: #left
                client_message = self.client.create_message('move', 'right')
                self.client.send(client_message)
            if keys[pygame.K_SPACE]: #shoot
                client_message = self.client.create_message('attack', '')
                self.client.send(client_message)
