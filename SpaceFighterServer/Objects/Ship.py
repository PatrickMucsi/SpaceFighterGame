
class Ship:
    def __init__(self, username, id, position, dimensions, type):
        self.username = username
        self.id = id
        self.position = position
        self.dimensions = dimensions
        self.mouse_position = None
        self.type = type
        self.movement_speed = 8
        self.velocity = (0,0)
        self.health = 100
        self.current_angle = 0
        self.current_weapon = 1
        self.lasers = []
        self.cool_downs = None
        self.cool_down_amounts = [1, 3, 7]
        self.health_bar = None
