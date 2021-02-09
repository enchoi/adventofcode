# Standard imports
import threading
import multiprocessing
from itertools import permutations

# 3rd party imports

# local imports
import day5


def get_amp():
    """ Create amplificator """
    opcodes = day5.get_int_code_configured()
    return opcodes


def process(opcodes):
    """ make apli run """
    opcodes.process()


def get_opcodes(nb):
    """ create and setup amplificator """
    # get codes
    with open("day7.input", "r") as fichier:
        codes = [int(x) for x in fichier.read().split(",")]
    # get amp
    amps = []
    for _ in range(nb):
        amp = get_amp()
        amp.set_codes(codes)
        amps.append(amp)
    return amps


if __name__ == '__main__':

    orders = list(permutations(range(5)))
    powers = []
    for order in orders:
        amps = get_opcodes(5)
        power = 0
        for amp, alu in zip(amps, order):
            conn_p, conn_c = multiprocessing.Pipe()
            amp.set_pipe(conn_c)
            thread = threading.Thread(target=process, args=(amp,))
            thread.start()
            conn_p.send(f"{alu}\n")
            conn_p.send(f"{power}\n")
            power = conn_p.recv()
            power = int(power)
        powers.append(power)
    print(max(powers))
