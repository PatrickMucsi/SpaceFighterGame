import pygame
import math
import time
import SpaceFighterTools as SFTools
from Objects.Laser import ShipLaser, BasicLaser, SuperLaser, MegaLaser
import Objects.SpaceFighterHUD as SFHUD

class Ship:
    def __init__(self, username, id, position, dimensions, type):
        self.username = username
        self.id = id
        self.position = position
        self.dimensions = dimensions
        self.mouse_position = None
        self.type = type
        self.movement_speed = 6
        self.velocity = (0,0)
        self.health = 100
        self.current_angle = 0
        self.current_weapon = 1
        self.lasers = []
        self.cool_downs = None
        self.cool_down_amounts = None
        self.health_bar = None

    def update(self):
        self.update_position()
        self.update_mouse_position(pygame.mouse.get_pos())
        self.current_angle = self.calculate_angle()
        if self.cool_downs == None:
            self.cool_downs = [time.time(), time.time(), time.time()]
        if self.health_bar != None:
            self.health_bar.update(self.health, (self.position[0], self.position[1] + self.dimensions[1]))
        if self.health <= 0:
            self.health = 100

    def draw(self, window, font, image):
        for laser in self.lasers:
            pygame.draw.rect(window, laser.color, pygame.Rect(laser.position, laser.dimensions))
        pygame.draw.rect(window, (255, 124, 100), pygame.Rect(self.position, self.dimensions))
        #window.blit(image, self.position)
        label = font.render(self.username, False, (255, 255, 255))
        position = label.get_rect(center=self.get_center())
        window.blit(label, (position[0], position[1] + (self.dimensions[1] / 2) + 23))
        if self.health_bar != None:
            self.health_bar.render(window)

    def was_hit(self, laser):
        self.health -= laser.damage

    def get_center(self):
        return (self.position[0] + (self.dimensions[0] / 2), self.position[1] + (self.dimensions[1] / 2))

    def to_string(self):
        return f'\t[Ship]\n[username] {self.username}\n[id] {self.id}\n[position] {self.position}\n[dimensions] {self.dimensions}'

    def calculate_angle(self):
        loc = ((self.position[0] + self.dimensions[0]) / 2, (self.position[1] + self.dimensions[1]) / 2)
        a = self.mouse_position[0] - loc[0]
        b = loc[1] - self.mouse_position[1]
        if b != 0:
            angle = math.degrees(math.atan(a/b))
            #angle = math.atan2(a, b)*180./math.pi
        else:
            angle = 0
        return angle

    def update_position(self):
        velocity_increment = .5
        if self.position != None:
            pos = list(self.position)
            pos[0] += self.velocity[0]
            pos[1] += self.velocity[1]
            self.position = tuple(pos)
        velocities = list(self.velocity)
        if velocities[0] < 0:
            velocities[0] += velocity_increment
        if velocities[0] > 0:
            velocities[0] -= velocity_increment
        if velocities[1] < 0:
            velocities[1] += velocity_increment
        if velocities[1] > 0:
            velocities[1] -= velocity_increment
        self.velocity = tuple(velocities)

    def move(self, direction):
        velocity_increment = 3
        velocities = list(self.velocity)
        if direction == 'left':
            if abs(self.velocity[0]) <= self.movement_speed:
                velocities[0] -= velocity_increment
        if direction == 'right':
            if abs(self.velocity[0]) <= self.movement_speed:
                velocities[0] += velocity_increment
        if direction == 'up':
            if abs(self.velocity[1]) <= self.movement_speed:
                velocities[1] -= velocity_increment
        if direction == 'down':
            if abs(self.velocity[1]) <= self.movement_speed:
                velocities[1] += velocity_increment
        self.velocity = tuple(velocities)

    def shoot(self, type):
        if type == 'ship':
            new_laser = ShipLaser(self.get_center(), self.mouse_position)
            self.lasers.append(new_laser)
        else:
            if self.cool_downs != None:
                if float(time.time() - self.cool_downs[self.current_weapon - 1]) >= float(self.cool_down_amounts[self.current_weapon - 1]):
                    new_laser = None
                    if self.current_weapon == 1:
                        new_laser = BasicLaser(self.get_center(), self.mouse_position)
                    elif self.current_weapon == 2:
                        new_laser = SuperLaser(self.get_center(), self.mouse_position)
                    elif self.current_weapon == 3:
                        new_laser = MegaLaser(self.get_center(), self.mouse_position)
                    if new_laser != None:
                        self.lasers.append(new_laser)
                        self.cool_downs[self.current_weapon - 1] = time.time()

    def update_mouse_position(self, position):
        self.mouse_position = position

    def create_health_bar(self):
        self.health_bar = SFHUD.HealthBar(self.health, (self.position[0], self.position[1] + self.dimensions[1]), 10, 50)
