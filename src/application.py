from game import Game

class Application:
    def __init__(self):
        self.Game = None

    def new_game(self):
        self.Game = Game()
    
    def run(self):
        """ Pelin Päivitys loopi """
        while True:
            status = self.Game.update()
            if status:
                break