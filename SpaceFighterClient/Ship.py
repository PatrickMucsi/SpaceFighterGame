import pygame
import math
import SpaceFighterTools as SFTools
from Laser import Laser

class Ship:
    def __init__(self, username, id, position, dimensions, type):
        self.username = username
        self.id = id
        self.position = position
        self.dimensions = dimensions
        self.mouse_position = None
        self.type = type
        self.movement_speed = 6
        self.health = 100
        self.current_angle = 0
        self.lasers = []

    def get_center(self):
        return (self.position[0] + (self.dimensions[0] / 2), self.position[1] + (self.dimensions[1] / 2))

    def to_string(self):
        return f'\t[Ship]\n[username] {self.username}\n[id] {self.id}\n[position] {self.position}\n[dimensions] {self.dimensions}'

    def draw(self, window, font):
        for laser in self.lasers:
            pygame.draw.rect(window, (255, 0, 0), pygame.Rect(laser.position, laser.dimensions))
        pygame.draw.rect(window, (255, 124, 100), pygame.Rect(self.position, self.dimensions))
        label = font.render(self.username, False, (255, 255, 255))
        position = label.get_rect(center=self.get_center())
        window.blit(label, (position[0], position[1] + (self.dimensions[1] / 2) + 23))

    def calculate_angle(self):
        loc = ((self.position[0] + self.dimensions[0]) / 2, (self.position[1] + self.dimensions[1]) / 2)
        # print(f'loc is {loc}')
        # print(f'[Ship] x: {loc[0]} y: {loc[1]}')
        # print(f'[Mouse]  x: {self.mouse_position[0]} y: {self.mouse_position[1]}')
        a = self.mouse_position[0] - loc[0]
        b = loc[1] - self.mouse_position[1]
        if b != 0:
            angle = math.degrees(math.atan(a/b))
            #angle = math.atan2(a, b)*180./math.pi
        else:
            angle = 0
        return angle

    def move(self, direction):
        pos = list(self.position)
        if direction == 'left':
            pos[0] -= self.movement_speed
        if direction == 'right':
            pos[0] += self.movement_speed
        if direction == 'up':
            pos[1] -= self.movement_speed
        if direction == 'down':
            pos[1] += self.movement_speed
        self.position = tuple(pos)

    def shoot(self):
        new_laser = Laser('basic', self.get_center(), self.mouse_position)
        self.lasers.append(new_laser)

    def update_mouse_position(self, position):
        self.mouse_position = position
        self.current_angle = self.calculate_angle()
