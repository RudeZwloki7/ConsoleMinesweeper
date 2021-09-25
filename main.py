from logic import Game

print("Enter number of mines and size of game field:")
inp = input()
mines, size = [int(val) for val in inp.split()]
game = Game(mines, size)

game.run()
