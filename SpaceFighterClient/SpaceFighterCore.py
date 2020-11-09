import pygame
import os, time, random, sys
import multiprocessing as mp

from Client import Client
from SpaceFighterShips import BasicShip

class SpaceFighterCore:
    def __init__(self):
        pygame.init()
        self.WIDTH = 750
        self.HEIGHT = 750
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Space Fighter Client v0.3')

        self.movement_queue = mp.Queue()
        self.client = Client(self.movement_queue)
        self.client.connect()

        self.player_one = BasicShip(300, 650)
        self.player_two = BasicShip(300, 650)
        #self.player_two = pygame.Rect(300, 650, 50, 50)

    def run(self):
        print('Starting game')
        running = True
        FPS = 60
        clock = pygame.time.Clock()
        player_offset = 500

        def redraw_window():
            self.WIN.fill((0,0,0))
            if not self.movement_queue.empty():
                message = self.movement_queue.get()
                p1 = message.get('p1')
                p2 = message.get('p2')
                p1_position = self.client.decode_message(p1)
                p2_position = self.client.decode_message(p2)
                if self.client.id == 0:
                    self.player_one.move(p1_position)
                    p2_position['y'] = p2_position.get('y') - player_offset
                    self.player_two.move(p2_position)
                if self.client.id == 1:
                    self.player_one.move(p2_position)
                    p1_position['y'] = p1_position.get('y') - player_offset
                    self.player_two.move(p1_position)

            self.player_one.render(self.WIN)
            self.player_two.render(self.WIN)
            pygame.display.update()

        def update():
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
                client_message = self.client.create_message('dir', 'left')
                self.client.send(client_message)
            if keys[pygame.K_d]: #left
                client_message = self.client.create_message('dir', 'right')
                self.client.send(client_message)
