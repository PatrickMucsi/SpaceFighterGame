from SpaceFighterCore import SpaceFighterCore

class SpaceFighter:
    def __init__(self):
        self.start_game()

    def start_game(self):
        self.game = SpaceFighterCore()
        self.game.run()


instance = SpaceFighter()
