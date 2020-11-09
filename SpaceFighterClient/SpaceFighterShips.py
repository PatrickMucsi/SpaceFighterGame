import pygame

class Ship:
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.ship = pygame.Rect(x, y, self.width, self.height)
        ####
        self.color = (123, 45, 67)

    def move(self, new_position):
        self.ship = self.ship.move(new_position.get('x') - self.ship.x, new_position.get('y') - self.ship.y)

    def render(self, window):
        pygame.draw.rect(window, self.color, self.ship)

class BasicShip(Ship):
    def __init__(self, x, y):
        width = 50
        height = 50
        super().__init__(x, y, width, height)
