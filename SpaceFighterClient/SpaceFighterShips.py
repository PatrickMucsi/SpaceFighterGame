import pygame
from SpaceFighterLasers import BasicLaser

class Ship:
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.ship = pygame.Rect(x, y, self.width, self.height)
        self.lasers = []
        ####
        self.color = (123, 45, 67)

    def shoot(self, position, direction):
        laser = BasicLaser(position, direction)
        self.lasers.append(laser)

    def move(self, new_position):
        self.ship = self.ship.move(new_position.get('x') - self.ship.x, new_position.get('y') - self.ship.y)

    def render(self, window):
        for laser in self.lasers:
            laser.render(window)
        pygame.draw.rect(window, self.color, self.ship)

    def update(self):
        for laser in self.lasers:
            laser.update()

    def get_position(self):
        return {'x': self.ship.x, 'y': self.ship.y}

    def update(self):
        for laser in self.lasers:
            if laser.laser.x > 750 or laser.laser.x < 0:
                self.lasers.remove(laser)
            else:
                laser.update()

class BasicShip(Ship):
    def __init__(self, x, y):
        width = 50
        height = 50
        super().__init__(x, y, width, height)
