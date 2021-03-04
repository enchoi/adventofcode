"""
Day 13

0 is an empty tile. No game object appears in this tile.
1 is a wall tile. Walls are indestructible barriers.
2 is a block tile. Blocks can be broken by the ball.
3 is a horizontal paddle tile. The paddle is indestructible.
4 is a ball tile. The ball moves diagonally and bounces off objects.

"""
# standard imports
import threading
import multiprocessing as mp

# local imports
import day5

with open("day13.input", "r") as fichier:
    codes = [int(x) for x in fichier.read().split(",")]

# get intcode...
opcodes = day5.get_int_code_configured()
opcodes.set_codes(codes)
pipe, other = mp.Pipe()
opcodes.set_pipe(other)

thread = threading.Thread(target=opcodes.process)
thread.daemon = True
thread.start()

tiles = []
try:
    while opcodes.is_running:
        # get from left
        left = pipe.recv()
        # get from top
        top = pipe.recv()
        # get material
        mat = pipe.recv()

        # save the tile
        tiles.append((left, top, mat))
except EOFError:
    pass

# How many block tiles are on the screen when the game exits?
print("Block: ", len([tile for tile in tiles if tile[2] == 2]))
