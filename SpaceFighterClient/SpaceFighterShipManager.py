from SpaceFighterClient import SpaceFighterClient
import SpaceFighterTools as SFTools
import Objects.SpaceFighterHUD as SFHUD
import sys
from Objects.Ship import Ship
import pygame
import time
import random

class SpaceFighterShipManager:
    def __init__(self, client):
        self.font = pygame.font.SysFont('Comic Sans MS', 23)
        self.client = client
        self.player = None
        self.players = []
        self.image = SFTools.scale_image(SFTools.load_image('assets', 'red_ship.png'), 50, 50)
        self.start_game()
        self.last_shot = time.time()
        self.damage_indicators = []

    def start_game(self):
        info = {'start': {'username' : self.client.username, 'id': self.client.id}}
        results = self.client.send_message('cmd', info)
        self.player = results.message if results.type == 'start' else None
        if self.player != None:
            self.player.create_health_bar()
        # TODO: if server does not return a player, retry

    def update(self):
        self.check_damage()
        self.player.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: #left
            self.player.move('left')
        if keys[pygame.K_d]: #right
            self.player.move('right')
        if keys[pygame.K_w]: #up
            self.player.move('up')
        if keys[pygame.K_s]: #down
            self.player.move('down')
        if keys[pygame.K_SPACE]: #down
            self.player.shoot('ship')
        if keys[pygame.K_1]:
            self.player.current_weapon = 1
        if keys[pygame.K_2]:
            self.player.current_weapon = 2
        if keys[pygame.K_3]:
            self.player.current_weapon = 3
        result = self.client.update_server(self.player)
        if result.type == 'positions':
            self.players = result.message
        for laser in self.player.lasers:
            if self.did_hit(laser):
                self.player.lasers.remove(laser)
            else:
                if laser.position[0] > 950 or laser.position[0] < 0 or laser.position[1] > 950 or laser.position[1] < 0:
                    self.player.lasers.remove(laser)
                else:
                    laser.update()

    def did_hit(self, laser):
        for player in self.players:
            if player.id != self.player.id:
                player_loc = pygame.Rect(player.position, player.dimensions)
                bullet = pygame.Rect(laser.position, laser.dimensions)
                if player_loc.colliderect(bullet):
                    self.create_damage_indicator(laser, player)
                    return True

        return False

    def create_damage_indicator(self, laser, player):
        #create random offset
        offset_limit = 15
        x = random.randrange(-offset_limit, offset_limit)
        y = random.randrange(-offset_limit, offset_limit)
        pos = player.get_center()
        random_offset = (pos[0] + x, pos[1] + y)
        self.damage_indicators.append(SFHUD.DamageIndicator(laser.damage, random_offset, time.time()))

    def check_damage(self):
        user = pygame.Rect(self.player.position, self.player.dimensions)
        for player in self.players:
            if player.id != self.player.id:
                for laser in player.lasers:
                    bullet = pygame.Rect(laser.position, laser.dimensions)
                    if user.colliderect(bullet):
                        self.player.was_hit(laser)
                        self.create_damage_indicator(laser, self.player)

    def render(self, window):
        if self.player != None:
            self.player.draw(window, self.font, self.image)
        for player in self.players:
            if player.id != self.player.id:
                player.draw(window, self.font, self.image)
        for indicator in self.damage_indicators:
            if time.time() - indicator.time < 1:
                window.blit(indicator.damage, indicator.position)
            else:
                self.damage_indicators.remove(indicator)
