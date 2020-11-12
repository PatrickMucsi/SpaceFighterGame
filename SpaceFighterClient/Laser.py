
class Laser:
    def __init__(self, type, position, direction):
        self.type = type
        self.position = position
        self.dimensions = (5, 5)
        self.direction = direction
        self.movement_speed = 12
        self.towards = -1 if self.direction[0] < self.position[0] else 1
        self.m = (direction[1] - position[1]) / (direction[0] - position[0])
        self.b = direction[1] - self.m * direction[0]

    def update(self):
        pos = list(self.position)
        pos[0] += (self.towards * self.movement_speed)
        pos[1] = (self.m * pos[0]) + self.b
        self.position = tuple(pos)
