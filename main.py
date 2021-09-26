from logic import Game
from logger import Logger
import sys

sys.stdout = Logger()

print("Would you like to test bot?\n1. Yes\n2. No")
mode = input().split()[0]

print("Enter number of mines and size of game field:")
inp = input()
mines, size = [int(val) for val in inp.split()]
game = Game(mode, mines, size)

game.run()
