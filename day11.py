
# standard imports
import time
import threading
import multiprocessing

# third party imports

# local imports
import day5


class Shell:
    def __init__(self, x, y, color=0):
        self.x = x
        self.y = y
        self.color = color

    def __eq__(self, other):
        if not isinstance(other, Shell):
            raise ValueError("Must compare shell")
        return (self.x == other.x) and (self.y == other.y)


def process(opcode):
    """ process the given opcodes """
    opcode.process()


class Hull_robot:
    """ emergency hull painting robot """

    directions = {
        "U": {0: "L", 1: "R"},
        "D": {0: "R", 1: "L"},
        "L": {0: "D", 1: "U"},
        "R": {0: "U", 1: "D"},
    }

    def __init__(self, opcode_brain):
        # mu current position
        self.x = 0
        self.y = 0

        # my current direction
        self.curr_dir = "U"

        # give me my brain
        self.codes = opcode_brain

        # set communication
        pipe1, pipe2 = multiprocessing.Pipe()
        self.pipe = pipe1
        self.codes.set_pipe(pipe2)

        # keep an eye on the shells
        self.shells = []

        # set codes
        with open("day11.input", "r") as fichier:
            codes = [int(x) for x in fichier.read().split(",")]
        self.codes.set_codes(codes)

    def move_forward(self):
        """ move forward... """
        if self.curr_dir == "U":
            self.y += 1
        if self.curr_dir == "L":
            self.x -= 1
        if self.curr_dir == "R":
            self.x += 1
        if self.curr_dir == "D":
            self.y -= 1

    def repaint(self, x, y, color):
        """ repaint the current shell """
        new_shell = Shell(x, y, color)
        for index, shell in enumerate(self.shells):
            if new_shell == shell:
                self.shells.pop(index)

        self.shells.append(new_shell)

    def search_shell(self, x, y):
        """ return the good shell """
        new_shell = Shell(x, y, 0)
        for shell in self.shells:
            if shell == new_shell:
                return shell
        return new_shell

    def execute(self):
        """ execute the program """
        thread = threading.Thread(target=process, args=(self.codes,))
        thread.daemon = True
        thread.start()
        repaint = {}
        try:
            while True:
                if self.codes.is_running:
                    # provide current color
                    color = self.search_shell(self.x, self.y).color
                    self.pipe.send(color)

                    # wait ?
                    # time.sleep(.01)

                    # get returns
                    new_color = self.pipe.recv()
                    new_direction = self.pipe.recv()
                    if color != new_color:
                        repaint[(self.x, self.y)] = repaint.get(
                            (self.x, self.y), 0) + 1

                    # repaint ?
                    self.repaint(self.x, self.y, new_color)
                    # change direction
                    self.curr_dir = self.directions[self.curr_dir][new_direction]
                    # move
                    self.move_forward()

                if not self.codes.is_running:
                    break
            thread.join()
        except KeyboardInterrupt:
            pass
        print("repaint: {}".format(len(repaint)))
        self.print_message()

    def print_message(self):
        """ print the message """
        x_s = [shell.x for shell in self.shells]
        y_s = [shell.y for shell in self.shells]
        x_min = min(x_s)
        x_max = max(x_s)
        y_min = min(y_s)
        y_max = max(y_s)
        for pos_y in range(y_min, y_max):
            for pos_x in range(x_min, x_max):
                print("#" if self.search_shell(
                    pos_x, pos_y).color else " ", end='')
            print("")


if __name__ == "__main__":
    codes = day5.get_int_code_configured()
    hull = Hull_robot(codes)
    hull.execute()
