"""
Pyöritää Application joka on pelin main loopi.
"""
from application import Application as App

def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()
    #from enum import Enum
    #class BoatTypes(Enum):
    #    lentotukialus = {"Size": 4, "Amount": 1},
    #    risteilija = {"Size": 3, "Amount": 2},
    #    havittaja = {"Size": 2, "Amount": 3},
    #    sukellusvene = {"Size": 1, "Amount": 4},
    #BoatTypes.risteilija.value[0]['Amount'] -= 1
    #print(BoatTypes.lentotukialus.value[0]['Amount'])