from SpaceFighterClient import SpaceFighterClient
import SpaceFighterTools as SFTools
import sys
from Ship import Ship
from Laser import Laser
import pygame
import time

class SpaceFighterShipManager:
    def __init__(self, client):
        self.font = pygame.font.SysFont('Comic Sans MS', 23)
        self.client = client
        self.player = None
        self.players = []
        self.image = SFTools.scale_image(SFTools.load_image('assets', 'red_ship.png'), 50, 50)
        self.start_game()
        self.last_shot = time.time()

    def start_game(self):
        info = {'start': {'username' : self.client.username, 'id': self.client.id}}
        results = self.client.send_message('cmd', info)
        self.player = results.message if results.type == 'start' else None
        # TODO: if server does not return a player, retry

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: #left
            self.player.move('left')
        if keys[pygame.K_d]: #right
            self.player.move('right')
        if keys[pygame.K_w]: #up
            self.player.move('up')
        if keys[pygame.K_s]: #down
            self.player.move('down')
        result = self.client.update_server(self.player)
        if result.type == 'positions':
            self.players = result.message
        self.player.update_mouse_position(pygame.mouse.get_pos())
        for laser in self.player.lasers:
            if laser.position[0] > 950 or laser.position[0] < 0 or laser.position[1] > 950 or laser.position[1] < 0:
                self.player.lasers.remove(laser)
            else:
                laser.update()

    def render(self, window):
        if self.player != None:
            self.player.draw(window, self.font)
        for player in self.players:
            if player.id != self.player.id:
                player.draw(window, self.font)
