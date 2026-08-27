import subprocess
import sys
from random import randint, choice
from boat import Boat, BoatTypes, BoatTypeIndex
import re
from enum import Enum
from color import Color

DEBUG = False


class Player:
    def __init__(self):
        self.Board: list[list[int]] = [[0 for _ in range(10)] for _ in range(10)]
        self.ShootingBoard: list[list[int]] = [[0 for _ in range(10)] for _ in range(10)]
        self.Boats: list[Boat] = []

        self.NeededBoatAmount = 0
        for boatType in BoatTypes.values():
            self.NeededBoatAmount += boatType['Amount']

        self.CurrentBoatTypeIndex: int = 0
        self.CurrentBoatType = BoatTypes[BoatTypeIndex[self.CurrentBoatTypeIndex]]

        if DEBUG:
            self.place_boats()

    def place_boat(self, boatType: dict[str, dict[str, int]], pos: tuple[int, int], rotation: int) -> bool:
        """ Laitaa Laivan self.Boats ja self.Boardiin """
        if not self.check_boatType_amount(boatType):
            return False

        new_boat = Boat(boatType, pos, rotation)
        if self.check_neighbors(new_boat):
            return False
        
        inside_board = True
        for pos in new_boat.get_positions():
            x, y = pos
            #print(f"PosX: {x} PosY: {y}")
            try:
                self.Board[y][x]
            except IndexError:
                inside_board = False

        if not inside_board:
            return False
        
        for pos in new_boat.get_positions():
            x, y = pos
            self.Board[y][x] = 1
            new_boat.add_cell(pos)

        self.Boats.append(new_boat)

        if not self.check_boatType_amount(boatType):
            self.CurrentBoatTypeIndex += 1

            indexRange = (len(BoatTypeIndex))
            self.CurrentBoatTypeIndex %= indexRange

            self.CurrentBoatType = BoatTypes[BoatTypeIndex[self.CurrentBoatTypeIndex]]
        
        return True

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
        neighbor_cells = []

        for pos in boat.get_positions():

            for dir in dirs:

                position = (pos[0] + dir[0], pos[1] + dir[1])
                x, y = position

                try:
                    if self.Board[y][x] == 1:
                        neighbor_cells.append(True)
                except IndexError:
                    neighbor_cells.append(False)

        if any(neighbor_cells):
            has_neighbors = True
        
        return has_neighbors
    
    def check_pos(self, pos: tuple[int, int]) -> bool:
        """ 
        Palautaa True jos osui muuten False. Palautaa True myös jos osui laivaan johon on osuttu.
        pos: tuple[int, int] (x, y)
        """
        x, y = pos
        
        if self.Board[y][x] == 1 or self.Board[y][x] == 2:
            return True
        return False

    def get_boat_by_pos(self, pos: tuple[int, int]) -> Boat:
        for boat in self.Boats:
            if pos in boat.Cells.keys():
                return boat
        return None
    
    def shoot(self, pos: tuple[int, int], otherPlayer) -> tuple[bool, bool]:
        """ Functio ampuu positioon ja jos osu niin palautaa True ja jos tuhos niin palautaa True """

        x, y = pos
        hit = False
        kill = False

        try:
            if self.check_pos(pos):
                boat = self.get_boat_by_pos(pos)
                boat.Cells[pos] = False

                self.Board[y][x] = 2
                otherPlayer.ShootingBoard[y][x] = 2
                hit = True

                if not boat.check_status():
                    kill = True

                if DEBUG:
                    boat.print_data()
            else:
                self.Board[y][x] = 3
                otherPlayer.ShootingBoard[y][x] = 3
        except IndexError:
            return (hit, kill)
        except AttributeError:
            return (hit, kill)
        return (hit, kill)
    
    def place_boats(self):
        """
        Tämä functio laitaa laivat randomisti peli laudalle. Yritää niin pitkää kunnes saa kaikki laitettua.
        """

        neededAmount = self.NeededBoatAmount
        placedAmount = 0
        placementFailsAmount = 0
            
        while placedAmount < neededAmount:
            posX = 0
            posy = 0
            rotation = 0

            if placementFailsAmount > 1000:
                self.clear_player()
                placedAmount = 0
                placementFailsAmount = 0
            else:
                for boatType in BoatTypes.values():
                    for _ in range(boatType['Amount']):
                        posX = randint(0, 9)
                        posy = randint(0, 9)
                        rotation = randint(0, 1)
                        success = self.place_boat(boatType, (posX, posy), rotation)

                        if success:
                            placedAmount += 1
                        else:
                            placementFailsAmount += 1
            if DEBUG:
                subprocess.run(["clear" if sys.platform == "linux" else "cls"], shell=True)
                print(f"Needed Amount: {neededAmount}")
                print(f"Placed Amount: {placedAmount}")
                print(f"Placement Fails Amount: {placementFailsAmount}")

    def clear_player(self):
        """ Palautaa Player Classin takas init muotoon. """
        self.Board: list[list[int]] = [[0 for _ in range(10)] for _ in range(10)]
        self.ShootingBoard: list[list[int]] = [[0 for _ in range(10)] for _ in range(10)]
        self.Boats: list[Boat] = []

    def is_dead(self) -> bool:
        boatStatusList = []
        for boat in self.Boats:
            boatStatusList.append(boat.check_status())
        #print(boatStatusList)
        return any(boatStatusList)


                    
            

                


class Cpu(Player):
    def __init__(self):
        super().__init__()
        self.first_hit_pos = None
        self.last_hit_pos = None
        self.found_dir = None

        self.choise_pattern: list[tuple[int, int]] = []

        for y in range(10):
            for x in range(10):
                if y % 2 == 0 and x % 2 == 0:
                    self.choise_pattern.append((x,y))
                elif y % 2 != 0 and x % 2 != 0:
                    self.choise_pattern.append((x,y))
        if DEBUG:
            print(self.choise_pattern)

        self.place_boats()

    def reverse_dir(self, dir: tuple[int, int]) -> tuple[int, int]:
        """ Kääntää annetun suunnan. """
        match dir:
            case (0, 1):
                return (0, -1)
            case (0, -1):
                return (0, 1)
            case (1, 0):
                return (-1, 0)
            case (-1, 0):
                return (1, 0)

    def play(self, otherPlayer):
        """ Tietokoneen pelaus functio joka hoitaa kaiken ampumisen jne. """

        dirs = [
            (0,-1),
            (0, 1),
            (-1,0),
            (1, 0),
        ]

        posX = 0
        posY = 0

        rand_dir = choice(dirs) if not self.found_dir else self.found_dir

        if self.first_hit_pos:
            while True:

                posX = (self.first_hit_pos[0] if not self.last_hit_pos else self.last_hit_pos[0]) + rand_dir[0]
                posY = (self.first_hit_pos[1] if not self.last_hit_pos else self.last_hit_pos[1]) + rand_dir[1]

                if self.ShootingBoard[posY][posX] == 2 or self.ShootingBoard[posY][posX] == 3:

                    rand_dir = choice(dirs)
                    posX = (self.first_hit_pos[0] if not self.last_hit_pos else self.last_hit_pos[0]) + rand_dir[0]
                    posY = (self.first_hit_pos[1] if not self.last_hit_pos else self.last_hit_pos[1]) + rand_dir[1]
                break
        else:
            position_trys = 0
            while True:
                random_position = choice(self.choise_pattern)
                posX = random_position[0]
                posY = random_position[1]

                if self.ShootingBoard[posY][posX] == 2 or self.ShootingBoard[posY][posX] == 3:
                    position_trys += 1
                    if position_trys > 5:
                        break
                else:
                    break
        
        hit, kill = otherPlayer.shoot((posX, posY), self)

        if hit:
            if self.first_hit_pos == None:
                self.first_hit_pos = (posX, posY)
            else:
                self.found_dir = rand_dir
            self.last_hit_pos = (posX, posY)

        if not hit and self.found_dir != None and self.last_hit_pos != None:
            self.last_hit_pos = self.first_hit_pos
            self.found_dir = self.reverse_dir(self.found_dir)

        if kill:
            self.last_hit_pos = None
            self.first_hit_pos = None
            self.found_dir = None

        if DEBUG:
            print(f"PosX: {posX} | PosY: {posY}")
            print(f"Hit: {hit}")
            print(f"Kill: {kill}")
            print("---------------")
            print(f"First Hit Pos: {self.first_hit_pos}")
            print(f"Last Hit Pos: {self.last_hit_pos}")
            print(f"Found Dir: {self.found_dir}")
    


class GameState(Enum):
    Placement = 0,
    Shooting = 1,

class Game:
    def __init__(self):
        self.Players: tuple[Player, Player] = (Player(), Cpu())
        self.Current_player_index: int = 0
        self.Current_player: Player = self.Players[self.Current_player_index]
        self.State: GameState = GameState.Placement

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
        """ Ampuu toisen pelaajan lautaan. """
        otherPlayer: Player = self.get_other_player()
        hit, kill = otherPlayer.shoot(pos, self.Current_player)

    def change_player(self):
        """ Vaihtaa Current_player valuen toiseen pelaajaan """

        if self.Current_player_index == 0:
            self.Current_player_index = 1
            self.Current_player = self.Players[self.Current_player_index]
        else:
            self.Current_player_index = 0
            self.Current_player = self.Players[self.Current_player_index]

    def clear_console(self):
        """ Tyhjentää terminaalin seuraavaa piirtoa varten """
        subprocess.run(["clear" if sys.platform == "linux" else "cls"], shell=True)
    
    def draw_all_boards(self):
        """ Debug piirto. Piirtää kaikki laudat """
        for player in self.Players:
            self.draw_player_boards(player)

    def draw_player_boards(self, player: Player):
        """ Piirtää pelaajan molemmat peli laudat. """
        self.draw_board(player.ShootingBoard, self.get_other_player(), "Shooting Board")
        self.draw_board(player.Board, self.Current_player, "Board")

    def draw_board(self, board: list[list[int]], player: Player, boardName: str):
        """ 
        Piirtää annetun laudan.
        board: list[list[int]]
        player: Player
        """

        print("\n\n")
        print(f"{boardName.center(22, " ")}")
        print("  A B C D E F G H I J")
        for y in range(len(board)):
            print(y, end=" ")
            for x in range(len(board[y])):
                match board[y][x]:
                    case 0:
                        print(f"{Color.OKBLUE}~{Color.ENDC}", end=" ")
                    case 1:
                        print("@", end=" ")
                    case 2:

                        boat = player.get_boat_by_pos((x,y))

                        if not boat.check_status():
                            print(f"{Color.OKGREEN}*{Color.ENDC}", end=" ")
                        else:
                            print("-", end=" ")

                    case 3:
                        print(f"{Color.FAIL}¤{Color.ENDC}", end=" ")
            print()
        print("---------------------")

    def convert_command(self, command: str) -> tuple[int, int, int]:
        """ Muuttaa komennon x,y ja suunta muotoon """

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

        x = 0
        y = 0
        dir = 0

        if len(parts) == 2:
            try:
                x = char_to_number[parts[0].lower()]
            except KeyError:
                x = 0
            y = int(parts[1])
        else:
            x = char_to_number[parts[0].lower()]
            y = int(parts[1])
            dir = direction[parts[2].lower()]

        return (x, y, dir)


    def update(self) -> bool:
        """ Pelin Update functio joka pyörii joka kerta uudestaan kun input annetaan. """

        self.clear_console()
        self.draw_player_boards(self.Current_player)

        if not isinstance(self.Current_player, Cpu):
            match self.State:
                case GameState.Placement:
                    print(f"Nykynen laiva: {BoatTypeIndex[self.Current_player.CurrentBoatTypeIndex]}")
                    print(f"Laivan Koko: {BoatTypes[BoatTypeIndex[self.Current_player.CurrentBoatTypeIndex]]['Size']}")
                    print()
                    print("Komento ohje: Sarake = Kirjain (a-j), Rivi = Numero (0-9), Suunta = Kirjain (D = Alas, S = Sivulle) | rand - komento laitaa kaikki laivat")
                    print()
                case GameState.Shooting:
                    print("Komento ohje: Sarake = Kirjain (a-j), Rivi = Numero (0-9)")
                    print()

            
            try:
                command = str(input("Anna positio: "))
            except KeyboardInterrupt:
                self.clear_console()
                return True
            
            if command == "rand":
                self.Current_player.place_boats()
                

            x, y, dir = self.convert_command(command)

            if self.State == GameState.Placement:

                self.place_boat(self.Current_player.CurrentBoatType, (x,y), dir)
                print(self.Current_player.NeededBoatAmount)

                if len(self.Current_player.Boats) == self.Current_player.NeededBoatAmount:
                    self.State = GameState.Shooting

            elif self.State == GameState.Shooting:

                self.shoot((x,y))
        else:
            self.Current_player.play(self.get_other_player())

        #print(self.State)

        if self.State == GameState.Shooting:
            self.change_player()

        if not self.Current_player.is_dead():
            self.clear_console()
            self.draw_player_boards(self.Current_player)
            return True


if __name__ == "__main__":
    print("Pyöritä main.py")
    input("Paina Enter")