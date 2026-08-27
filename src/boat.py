BoatTypes = {
    "lentotukialus": {"Size": 5, "Amount": 1},
    "risteilija": {"Size": 4, "Amount": 2},
    "havittaja": {"Size": 3, "Amount": 3},
    "sukellusvene": {"Size": 2, "Amount": 4},
}

BoatTypeIndex = {
    0: "lentotukialus",
    1: "risteilija",
    2: "havittaja",
    3: "sukellusvene"
}


class Boat:
    def __init__(self, boat_type: dict[str, dict[str, int]], position: tuple[int, int], rotation: int):
        self.BoatType = boat_type
        self.Size: int = boat_type['Size']
        self.Position: tuple[int, int] = position
        self.Rotation: int = rotation
        self.Cells: dict[tuple[int, int], bool] = {}

    def check_status(self) -> bool:
        """ Tarkistaa onko kaikki True tai False. Jos kaikki on False palauttaa False """
        return any(self.Cells.values())

    def add_cell(self, pos: tuple[int, int]):
        """ Lisää positionin laivan Cells sanakirjaan {pos: True} """
        if pos not in self.Cells:
            self.Cells[pos] = True

    def get_positions(self) -> list[tuple[int, int]]:
        """ 
            Palauttaa laivan kaikki positiot rotation ja sizen mukaan. 
            Lista pitää sisällä tuple[int, int]
        """
        current_pos: tuple[int, int] = self.Position
        direction: tuple[int, int] = self.get_dir()
        positions: list[tuple[int, int]] = []

        for _ in range(self.Size):
            positions.append(current_pos)
            current_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])

        return positions
            
    def get_dir(self):
        """ Palauttaa suunnan Rotation perusteella. return tuple[int, int] """
        match self.Rotation:
            case 0:
                return (0, 1)
            case 1:
                return (1, 0)
            case _:
                return (0, 1)

    def print_data(self):
        print(f"Size: {self.Size}")
        print(f"Cells: {self.Cells}")