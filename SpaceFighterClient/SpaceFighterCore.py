from SpaceFighterClient import SpaceFighterClient
from SpaceFighterShipManager import SpaceFighterShipManager
from Objects.SpaceFighterHUD import SpaceFighterHUD
import SpaceFighterTools as SFTools
import sys
import pygame
import time

class SpaceFighterCore:
    def __init__(self):
        username = input('Enter a username: ')
        pygame.init()
        self.WIDTH = 950
        self.HEIGHT = 950
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Space Fighter v0.6')

        self.client = SpaceFighterClient(username)
        self.ship_manager = SpaceFighterShipManager(self.client)
        self.HUD = SpaceFighterHUD(self.ship_manager.player)
        self.background = SFTools.load_image('assets', 'background.png')
        self.run()

    def run(self):
        print('Starting game')
        running = True
        FPS = 60
        clock = pygame.time.Clock()

        def redraw_window():
            self.WIN.blit(self.background, (0,0))
            self.ship_manager.render(self.WIN)
            self.HUD.render(self.WIN)
            pygame.display.update()

        def update():
            self.ship_manager.update()
            self.HUD.update()

        while running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.client.disconnect()
                    running = False
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.ship_manager.player.shoot('none')

            update()
            redraw_window()
