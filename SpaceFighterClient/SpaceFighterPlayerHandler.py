from SpaceFighterShips import BasicShip

class SpaceFighterPlayerHandler:
    def __init__(self, movement_queue):
        self.movement_queue = movement_queue
        self.player_offset = 500

        self.player_one = BasicShip(375, 375)
        self.player_two = BasicShip(375, 375)

    def render(self, window):
        self.player_one.render(window)
        self.player_two.render(window)

    def process_network_message(self, client, message):
        p1 = message.get('p1')
        p2 = message.get('p2')
        p1_position = client.decode_message(p1)
        p2_position = client.decode_message(p2)
        print(f'client id:\t{client.id}\np1 pos:\t{p1_position}\np2 pos:\t{p2_position}')
        if client.id == 0:
            self.player_one.move(p1_position)
            p2_position['y'] = p2_position.get('y') - self.player_offset
            self.player_two.move(p2_position)
        if client.id == 1:
            self.player_one.move(p2_position)
            p1_position['y'] = p1_position.get('y') - self.player_offset
            self.player_two.move(p1_position)

    def update(self, client):
        if not self.movement_queue.empty():
            message = self.movement_queue.get()
            p1 = message.get('p1')
            p2 = message.get('p2')
            p1_position = client.decode_message(p1)
            p2_position = client.decode_message(p2)
            if client.id == 0:
                self.player_one.move(p1_position)
                p2_position['y'] = p2_position.get('y') - self.player_offset
                self.player_two.move(p2_position)
            if client.id == 1:
                self.player_one.move(p2_position)
                p1_position['y'] = p1_position.get('y') - self.player_offset
                self.player_two.move(p1_position)
