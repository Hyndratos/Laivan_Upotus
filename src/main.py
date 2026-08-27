"""
Pyöritää Application joka on pelin main loopi.
"""
from application import Application as App

def main():
    app = App()
    app.new_game()
    app.run()

if __name__ == "__main__":
    main()