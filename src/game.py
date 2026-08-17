from boat import Boat, BoatTypes

class Player:
    def __init__(self):
        self.Board: list[list[int]] = [[0 for _ in range(10)] for _ in range(10)]
        self.Boats: list[Boat] = []

    def place_boat(self, boatType: BoatTypes):
        pass
        

    def check_pos(self, pos: tuple[int, int]) -> bool:
        pass
    
    def shoot(self, pos: tuple[int, int]):
        pass

class Game:
    def __init__(self):
        self.Players: tuple[Player, Player] = (Player(), Player())
        self.Current_player_index: int = 0
        self.Current_player: Player = self.Players[self.Current_player_Index]

    def get_other_player(self) -> Player:
        for otherPlayer in self.Players:
            if otherPlayer != self.Current_player:
                return otherPlayer
    
    def place_boat(self, boat: Boat):
        self.Current_player.place_boat(boat)
    
    def shoot(self, pos: tuple[int, int]):
        otherPlayer: Player = self.get_other_player()
        otherPlayer.shoot(pos)

    def change_player(self):
        if self.Current_player_index == 0:
            self.Current_player_index = 1
            self.Current_player = self.Players[self.Current_player_index]
        else:
            self.Current_player_index = 0
            self.Current_player = self.Players[self.Current_player_index]

    def update(self):
        pass