import subprocess
import sys
from random import randint
from boat import Boat, BoatTypes
import re
from enum import Enum

DEBUG = True


class Player:
    def __init__(self):
        self.Board: list[list[int]] = [[0 for _ in range(10)] for _ in range(10)]
        self.ShootingBoard: list[list[int]] = [[0 for _ in range(10)] for _ in range(10)]
        self.Boats: list[Boat] = []
        if DEBUG:
            self.place_boat(BoatTypes["lentotukialus"], (4,3), 0)
            self.place_boat(BoatTypes["risteilija"], (6,3), 0)

    def place_boat(self, boatType: dict[str, dict[str, int]], pos: tuple[int, int], rotation: int):
        """ Laitaa Laivan self.Boats ja self.Boardiin """
        if not self.check_boatType_amount(boatType):
            return

        new_boat = Boat(boatType, pos, rotation)
        if self.check_neighbors(new_boat):
            return
        
        inside_board = False
        for pos in new_boat.get_positions():
            x, y = pos
            if (x >= 0 and x <= len(self.Board[0]) - 1) and (y >= 0 and y <= len(self.Board) - 1):
                inside_board = True
            else:
                inside_board = False

        if not inside_board:
            return
        
        for pos in new_boat.get_positions():
            x, y = pos
            self.Board[y][x] = 1
            new_boat.add_cell(pos)
        self.Boats.append(new_boat)

    def check_boatType_amount(self, boatType: dict[str, int]) -> bool:
        """ palautaa True jos laiva tyyppiä voi vielä laitaa. """
        count = 0
        for boat in self.Boats:
            if boat.BoatType["Size"] == boatType["Size"]:
                count += 1
        
        if count < boatType["Amount"]:
            return True
        return False

    def check_neighbors(self, boat: Boat) -> bool:
        """ 
        Tämä functio käy läpi jokasen viereisen naapurin ja katsoo onko siinä laivaa.
        Palautaa False jos laivalla ei ole naapureita. Muuten palautaa True.

        (-1,-1)(0,-1)(1,-1)
        (-1, 0)      (1, 0)
        (-1, 1)(0, 1)(1, 1)
        """
        
        dirs = [
            (0,1),
            (1,0),
            (0,-1),
            (-1,0),
            (1,1),
            (-1,-1),
            (1,-1),
            (-1,1)
        ]
        has_neighbors = False

        for pos in boat.get_positions():

            for dir in dirs:

                position = (pos[0] + dir[0], pos[1] + dir[1])
                x, y = position

                if self.Board[y][x] == 1:
                    has_neighbors = True
                    break
        
        return has_neighbors
    
    def check_pos(self, pos: tuple[int, int]) -> bool:
        """ Palautaa True jos osui muuten False. Palautaa True myös jos osui laivaan johon on osuttu """
        x, y = pos
        if self.Board[y][x] == 1 or self.Board[y][x] == 2:
            return True
        return False

    def get_boat_by_pos(self, pos: tuple[int, int]) -> Boat:
        for boat in self.Boats:
            if any(boat.Cells.keys()):
                return boat
        return None
    
    def shoot(self, pos: tuple[int, int], otherPlayer) -> tuple[bool, bool]:
        x, y = pos
        hit = False
        kill = False
        if self.check_pos(pos):
            boat = self.get_boat_by_pos(pos)
            boat.Cells[pos] = False

            self.Board[y][x] = 2
            otherPlayer.ShootingBoard[y][x] = 2
            hit = True

            if not boat.check_status():
                kill = True
        else:
            self.Board[y][x] = 3
            otherPlayer.ShootingBoard[y][x] = 3
            hit = True
        
        return (hit, kill)
                


class Cpu(Player):
    def __init__(self):
        super().__init__()
        self.first_hit_pos = None
        self.last_hit_pos = None

    def play(self, otherPlayer):
        posX = (0,0)
        posY = (0,0)

        for y in range(len(self.Board)):
            for x in range(len(self.Board[y])):
                if self.ShootingBoard[y][x] != 0:
                    continue
                if y % 2 == 0 and x % 2 == 0:
                    posX = x
                    posY = y
                elif y % 2 != 0 and x % 2 != 0:
                    posX = x
                    posY = y
                    
                #if (x % 2 == 0 and y % 2 == 0) and self.ShootingBoard[y][x] == 0:
                #    posX = x
                #    posY = y
        
        hit, kill = otherPlayer.shoot((posX,posY), self)

        if hit:
            if self.first_hit_pos == None:
                self.first_hit_pos = (x, y)

        if kill:
            self.last_hit_pos = None
            self.first_hit_pos = None
    


class GameState(Enum):
    Placement = 0,
    Shooting = 1,

class Game:
    def __init__(self):
        self.Players: tuple[Player, Player] = (Player(), Cpu())
        self.Current_player_index: int = 0
        self.Current_player: Player = self.Players[self.Current_player_index]
        self.State: GameState = GameState.Shooting

    def get_other_player(self) -> Player:
        """
        Tämä functio vertaa current_playeriä toisen pelaajaan ja palautaa sen toisen.
        """

        for otherPlayer in self.Players:
            if otherPlayer != self.Current_player:
                return otherPlayer
    
    def place_boat(self, boatType: dict[str, dict[str, int]], pos: tuple[int, int], rotation: int):
        self.Current_player.place_boat(boatType, pos, rotation)
    
    def shoot(self, pos: tuple[int, int]):
        otherPlayer: Player = self.get_other_player()
        hit, kill = otherPlayer.shoot(pos, self.Current_player)

    def change_player(self):
        if self.Current_player_index == 0:
            self.Current_player_index = 1
            self.Current_player = self.Players[self.Current_player_index]
        else:
            self.Current_player_index = 0
            self.Current_player = self.Players[self.Current_player_index]

    def clear_console(self):
        """ Tyhjentää terminaalin seurvaa piirtoa varten """
        subprocess.run(["clear" if sys.platform == "linux" else "cls"], shell=True)
    
    def draw_all_boards(self):
        for player in self.Players:
            self.draw_player_boards(player)

    def draw_player_boards(self, player: Player):
        self.draw_board(player.ShootingBoard)
        self.draw_board(player.Board)

    def draw_board(self, board):
        print("\n\n")
        print("  A B C D E F G H I J")
        for y in range(len(board)):
            print(y, end=" ")
            for x in range(len(board[y])):
                match board[y][x]:
                    case 0:
                        print("#", end=" ")
                    case 1:
                        print("@", end=" ")
                    case 2:
                        print("O", end=" ")
                    case 3:
                        print("X", end=" ")
            print()
        print("---------------------")

    def convert_command(self, command: str) -> tuple[int, int, int]:
        char_to_number = {
            "a": 0,
            "b": 1,
            "c": 2,
            "d": 3,
            "e": 4,
            "f": 5,
            "g": 6,
            "h": 7,
            "i": 8,
            "j": 9, 
        }
        direction = {
            "d": 0,
            "s": 1
        }

        parts: tuple[str, str, str] = re.findall(r'\D+|\d+', command)

        try: int(parts[1])
        except: return (0,0,0)
        dir = 0
        if len(parts) == 2:
            x = char_to_number[parts[0].lower()]
            y = int(parts[1])
        else:
            dir = direction[parts[2].lower()]

        return (x, y, dir)


    def update(self):
        """ Pelin Update functio joka pyörii joka kerta uudestaan kun input annetaan. """
        #self.clear_console()
        print(f"Current Player: {type(self.Current_player)}")
        self.draw_player_boards(self.Current_player)
        #self.draw_all_boards()

        if not isinstance(self.Current_player, Cpu):
            command = str(input("Anna positio: "))
            x, y, dir = self.convert_command(command)
            if self.State == GameState.Placement:
                self.place_boat(BoatTypes["lentotukialus"], (x,y), dir)
            elif self.State == GameState.Shooting:
                self.shoot((x,y))
        else:
            self.Current_player.play(self.get_other_player())
        self.change_player()