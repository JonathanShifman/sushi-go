class Player(object):
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def play(self, game_knowledge):
        raise NotImplemented()