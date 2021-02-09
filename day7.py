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

    orders = list(permutations(range(5, 10)))
    powers = []
    for order in orders:
        amps = get_opcodes(5)
        power = 0
        pipes = []
        threads = []
        # setup amps
        for amp, alumage in zip(amps, order):
            conn1, conn2 = multiprocessing.Pipe()
            amp.set_pipe(conn2)
            pipes.append(conn1)
            conn1.send(alumage)

        # start threading
        for amp in amps:
            thread = threading.Thread(target=process, args=(amp,))
            thread.start()
            threads.append(thread)

        # begin amplification
        while True:
            running = []
            for amp, pipe, thread in zip(amps, pipes, threads):
                pipe.send(power)
                power = int(pipe.recv())
                running.append(amp.is_running)
            if not all(running):
                break
        for thread in threads:
            thread.join()

        powers.append(power)
    print(max(powers))
