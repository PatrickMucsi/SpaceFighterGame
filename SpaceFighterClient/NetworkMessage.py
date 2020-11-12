class NetworkMessage:
    def __init__(self, type, message):
        self.type = type
        self.message = message

    def to_string(self):
        return f'[Type]\t{self.type}\n[Message]\t{self.message}'
