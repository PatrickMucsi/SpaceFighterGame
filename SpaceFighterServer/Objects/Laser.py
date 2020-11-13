import math

class Laser:
    def __init__(self, type, position, direction):
        self.type = type
        self.position = position
        self.dimensions = dimesions
        self.direction = direction
        self.movement_speed = speed
        self.delta = self.calculate_delta()

    def calculate_delta(self):
        angle = math.atan2(self.direction[1] - self.position[1], self.direction[0] - self.position[0])
        delta_x = math.cos(angle) * self.movement_speed
        delta_y = math.sin(angle) * self.movement_speed
        return (delta_x, delta_y)

class ShipLaser(Laser):
    def __init__(self, position, direction):
        movement_speed = 30
        dimensions = (2, 2)
        self.damage = 0.5
        super().__init__('ship', position, dimensions, direction, movement_speed, damage)

class BasicLaser(Laser):
    def __init__(self, position, direction):
        movement_speed = 25
        dimensions = (5, 5)
        self.damage = 5
        super().__init__('basic', position, dimensions, direction, movement_speed, damage)

class SuperLaser(Laser):
    def __init__(self, position, direction):
        movement_speed = 20
        dimensions = (15, 15)
        self.damage = 10
        super().__init__('super', position, dimensions, direction, movement_speed, damage)

class MegaLaser(Laser):
    def __init__(self, position, direction):
        movement_speed = 15
        dimensions = (25, 25)
        damage = 40
        self.color = (255, 0, 255)
        super().__init__('mega', position, dimensions, direction, movement_speed, damage)
