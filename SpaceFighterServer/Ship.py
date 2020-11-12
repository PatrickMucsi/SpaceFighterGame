
class Ship:
    def __init__(self, username, id, position, dimensions, type):
        self.username = username
        self.id = id
        self.position = position
        self.dimensions = dimensions
        self.mouse_position = None
        self.type = type
        self.movement_speed = 8
        self.health = 100
        self.current_angle = 0
        self.lasers = []

    def to_string(self):
        return f'\t[Ship]\n[username] {self.username}\n[id] {self.id}\n[position] {self.position}'
