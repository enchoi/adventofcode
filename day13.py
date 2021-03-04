"""
Day 13

0 is an empty tile. No game object appears in this tile.
1 is a wall tile. Walls are indestructible barriers.
2 is a block tile. Blocks can be broken by the ball.
3 is a horizontal paddle tile. The paddle is indestructible.
4 is a ball tile. The ball moves diagonally and bounces off objects.

"""
# standard imports
import os
import time
import threading
import multiprocessing as mp

# thrid party imports
import keyboard

# local imports
import day5


def find(x, y):
    """ find the right tile """
    try:
        return tiles[(x, y)]
    except KeyError:
        return 0


def controller(pipe, go):
    while True:
        if keyboard.is_pressed("left"):
            # while keyboard.is_pressed("left"):
            #     pass

            pipe.send(-1)
        if keyboard.is_pressed("right"):
            # while keyboard.is_pressed("right"):
            #     pass
            pipe.send(1)
        if keyboard.is_pressed("espace"):
            go.append(True)
            pipe.send(0)
            return
        else:
            pass
        time.sleep(0.5)


def clear(): return os.system('clear')


def print_(tiles):
    """ print the message """
    while True:
        try:
            x_s = [tile[0] for tile in tiles.keys()]
            y_s = [tile[1] for tile in tiles.keys()]
            x_min = 0
            x_max = max(x_s)
            y_min = 0
            y_max = max(y_s)
            string = "\33[2J"
            for pos_y in range(y_min, y_max+1):
                for pos_x in range(x_min, x_max+1):
                    string += repr_tiles[find(pos_x, pos_y)]
                string += "\n"
            print(string)
            os.sys.stdout.flush()
            time.sleep(0.008)
        except:
            pass

    # string += str(find(-1, 0))

    # with open("day13.ouput", "w") as fichier:
    #     fichier.write(string)


with open("day13.input", "r") as fichier:
    codes = [int(x) for x in fichier.read().split(",")]

repr_tiles = {0: " ",
              1: "W",
              2: "B",
              3: "=",
              4: "O"}

# get intcode...
opcodes = day5.get_int_code_configured()
opcodes.set_codes(codes)
pipe, other = mp.Pipe()
opcodes.set_pipe(other)

tiles = dict()
thread = threading.Thread(target=opcodes.process)
thread.daemon = True
thread.start()

go = []
thread_keyboard = threading.Thread(target=controller, args=(pipe, go))
thread_keyboard.daemon = True
thread_keyboard.start()
thread_screen = threading.Thread(target=print_, args=(tiles,))
thread_screen.daemon = True
thread_screen.start()
instructions = []
score = []
try:
    while True:
        # get from left
        x = pipe.recv()
        # get from top
        y = pipe.recv()
        # get material
        mat = pipe.recv()

        # save the tile
        # if x == -1 and not y:
        #     print("Score : ", mat)
        # else:
        tiles[(x, y)] = mat

        instructions.append((x, y, mat))
        if x == -1:
            score.append(mat)
        # print_(tiles)
        if go and mat in [4]:
            try:
                me = [key for key, value in tiles.items() if value == 3][0]
                ball = [key for key, value in tiles.items() if value == 4][0]
                if me[0] > ball[0]:
                    pipe.send(-1)
                elif me[0] < ball[0]:
                    pipe.send(1)
                else:
                    pipe.send(0)
                # time.sleep(0.001)
            except KeyboardInterrupt:
                raise
            except:
                pass
except (EOFError, KeyboardInterrupt) as exp:
    print(exp)

# clear()
print(instructions[-10:])
print(score[-10:])
# How many block tiles are on the screen when the game exits?
print("Block: ", len([pos for pos, tile in tiles.items() if tile == 2]))
print("Score: ", tiles.get((-1, 0), 0))
