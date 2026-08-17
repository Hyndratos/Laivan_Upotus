from boat import Boat

class Player:
    def __init__(self):
        self.Board: list[list[int]] = [[0 for _ in range(10)] for _ in range(10)]
        self.Boats: list[Boat] = []

    def place_boat(self, boat: Boat):
        pass

    def check_pos(self, pos: tuple[int, int]) -> bool:
        pass
    
    def shoot(sefl, pos: tuple[int, int]):
        pass

class Game:
    def __init__(self):
        self.Players: tuple[Player, Player] = (Player(), Player())

    def get_other_player(self, player: Player) -> Player:
        for otherPlayer in self.Players:
            if otherPlayer != player:
                return otherPlayer
    
    def place_boat(self, player: Player, boat: Boat):
        player.place_boat(boat)

    def check_pos(self, player: Player, pos: tuple[int, int]) -> bool:
        player.check_pos(pos)
    
    def shoot(sefl, player: Player, pos: tuple[int, int]):
        player.shoot(pos)

    def update(self):
        pass