from SpaceFighterClient import SpaceFighterClient
from SpaceFighterShipManager import SpaceFighterShipManager
from Objects.SpaceFighterHUD import SpaceFighterHUD
import SpaceFighterTools as SFTools
import sys
import pygame
import time

    # self.client = SpaceFighterClient()
    # self.username = 'fart knocker'
    # self.id = uuid.uuid4()
    # info = {'start': {'username' : self.username, 'id': self.id}}
    # results = self.client.send_message('cmd', info)
    # ship = results.message if results.type == 'start' else None
    # if ship != None:
    #     print(ship.to_string())
    # self.client.client.disconnect()


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
        self.background = SFTools.scale_image(SFTools.load_image('assets', 'background.png'), 950, 850)
        self.run()

    def run(self):
        print('Starting game')
        running = True
        FPS = 60
        clock = pygame.time.Clock()

        def redraw_window():
            #print('redrawing')
            self.WIN.fill((0,0,0))
            #self.WIN.blit(self.background, (0,0))
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
                    #if time.time() - self.ship_manager.last_shot > 2:
                    self.ship_manager.player.shoot('none')
                        #self.ship_manager.last_shot = time.time()

            update()
            redraw_window()
