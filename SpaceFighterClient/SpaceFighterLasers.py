import pygame

class Laser:
    def __init__(self, type, position, dimensions, direction, damage):
        self.type
        self.damage = damage
        self.direction = direction
        self.laser = pygame.Rect(position, dimensions)

    def render(self, window):
        pygame.draw.rect(window, (10, 10, 10), self.laser)

    def update(self):
        self.laser = self.laser.move(0, self.laser.y - self.direction)


class BasicLaser(Laser):
    def __init__(self, position, direction):
        damage = 25
        dimensions = (10, 10)
        super().__init__('basic_laser', position, dimensions, direction, damage)
