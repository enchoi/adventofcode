import sys
from copy import deepcopy
from itertools import zip_longest


class Opcodes():
    """ A test for day5 """

    def __init__(self, codes=None):
        self._cursor = 0
        self._codes = codes
        self._methods = {}
        self.is_running = True
        self.debug = False
        self._com_pipe = None
        self.rel_offset = 0
        self._len_code = 0

    # def write(self, key, value, mode=0):
    #     """ write depending mode
    #     0: Position
    #     1: Immediate (can't be)
    #     2: related"""
    #     if not mode:
    #         self._codes[key] = value
    #     else:
    #         self._code[self.rel_offset] = value

    def set_pipe(self, pipe):
        """ set a communication pipe """
        self._com_pipe = pipe

    def is_pipe(self):
        """ check if a pipe is present """
        return self._com_pipe is not None

    def read_pipe(self):
        """ return first object in pipe """
        return self._com_pipe.recv()

    def write_pipe(self, item):
        """ write item in pipe """
        self._com_pipe.send(item)

    def set_codes(self, codes):
        """ Set codes instruction """
        self._codes = [0] * 500_000
        self._len_code = len(codes)
        for index, data in enumerate(deepcopy(codes)):
            self._codes[index] = data

    def in_debug(self, boolean):
        """ go in debug ? """
        self.debug = boolean

    def __getitem__(self, key):
        return self._codes[key]

    def __setitem__(self, key, value):
        self._codes[key] = value

    def _read(self,):
        """ read data 1b1 """
        data = self._codes[self._cursor]
        self._cursor += 1
        return data

    def read(self, mode):
        """ read with mode """
        data = self._read()
        if mode == 1:
            return data
        if mode == 2:
            return self._codes[self.rel_offset + data]
        return self._codes[data]

    def reset(self):
        """ reset cursor """
        self._cursor = 0
        self.rel_offset = 0

    def jump_to(self, address):
        """ jump to address """
        self._cursor = address

    def stop(self):
        """ stop processing """
        self.is_running = False

    def add_methods(self, instr, method, params_nb, ret):
        """ add a method """
        self._methods[instr] = (params_nb, method, ret)

    def set_relatif_offset(self, offset):
        """ ajust the relatif offset """
        self.rel_offset = offset

    def process(self):
        """ process data """
        while self.is_running:
            # read instruction
            instr_params = self.read(True)

            # cut insctruction part
            instr = int(f"{instr_params:0>#2}"[-2:])

            # get parameter number to get modes
            nb_arg, method, nb_ret = self._methods[instr]

            # compute modes
            modes = f"{{instr_params:0>#{nb_arg+nb_ret+2}}}".format(instr_params=instr_params)[:-2]
            modes = modes[::-1]
            arg_modes = modes[:nb_arg]
            ret_modes = modes[nb_arg:]

            # read args
            args = []
            for mode in arg_modes:
                args.append(self.read(int(mode)))
            for mode in ret_modes:
                mode = int(mode)
                # position
                if not mode:
                    args.append(self._read())
                # related offset
                elif mode == 2:
                    args.append(self.rel_offset + self._read())

            if self.debug:
                print("\n\n\nNew instruction")
                print(f"instr_params: {instr_params}")
                print(f"instr: {instr}")
                print(f"modes: {modes}")
                print(f"arg_modes: {arg_modes}")
                print(f"ret_modes: {ret_modes}")
                print(f"args: {args}")

            method(self, *args)


def add(opcode, x, y, ret):
    """ add x to y and return data in ret """
    opcode[ret] = x + y


def multiply(opcode, x, y, ret):
    """ multiply x to y and return data in ret """
    opcode[ret] = x * y


def inputt(opcode, ret):
    """ get ipnut and safe at ret """
    if not opcode.is_pipe():
        data = int(input("Enter a number:\n"))
    else:
        data = int(opcode.read_pipe())
    opcode[ret] = data


def outputt(opcodes, ret):
    """ return opcode memory[ret] """
    if not opcodes.is_pipe():
        print(ret)
    else:
        opcodes.write_pipe(ret)


def jump_if_true(opcodes, test, jump):
    """ jump if true """
    if test:
        opcodes.jump_to(jump)


def jump_if_false(opcodes, test, jump):
    """ jump if false """
    if not test:
        opcodes.jump_to(jump)


def less_than(opcodes, param1, param2, ret):
    """ jump if less """
    opcodes[ret] = int(param1 < param2)


def equals(opcodes, param1, param2, ret):
    """ jump if equal """
    opcodes[ret] = int(param1 == param2)


def stop(opcode):
    """ stop processing """
    opcode.stop()


def set_relatif_offset(opcodes, offset):
    """ set the relatif offset """
    opcodes.set_relatif_offset(opcodes.rel_offset + offset)


def get_int_code_configured():
    """ return int code configured """
    opcodes = Opcodes()
    opcodes.add_methods(1, add, 2, 1)
    opcodes.add_methods(2, multiply, 2, 1)
    opcodes.add_methods(3, inputt, 0, 1)
    opcodes.add_methods(4, outputt, 1, 0)
    opcodes.add_methods(5, jump_if_true, 2, 0)
    opcodes.add_methods(6, jump_if_false, 2, 0)
    opcodes.add_methods(7, less_than, 2, 1)
    opcodes.add_methods(8, equals, 2, 1)
    opcodes.add_methods(9, set_relatif_offset, 1, 0)
    opcodes.add_methods(99, stop, 0, 0)
    return opcodes


if __name__ == '__main__':
    datas = [3, 225, 1, 225, 6, 6, 1100, 1, 238, 225, 104, 0, 1102, 78, 40, 225, 1102,
             52, 43, 224, 1001, 224, -2236, 224, 4, 224, 102, 8, 223, 223, 101, 4, 224, 224,
             1, 224, 223, 223, 1, 191, 61, 224, 1001, 224, -
             131, 224, 4, 224, 102, 8, 223, 223,
             101, 4, 224, 224, 1, 223, 224, 223, 1101, 86, 74, 225, 1102, 14, 76, 225, 1101, 73,
             83, 224, 101, -156, 224, 224, 4, 224, 102, 8, 223, 223, 101, 6, 224, 224, 1, 224,
             223, 223, 1102, 43, 82, 225, 2, 196, 13, 224, 101, -6162, 224, 224, 4, 224, 102,
             8, 223, 223, 101, 5, 224, 224, 1, 223, 224, 223, 1001, 161, 51, 224, 101, -70,
             224, 224, 4, 224, 102, 8, 223, 223, 1001, 224, 1, 224, 1, 224, 223, 223,
             102, 52, 187, 224, 1001, 224, -832, 224, 4, 224, 102, 8, 223, 223, 101,
             1, 224, 224, 1, 224, 223, 223, 1102, 19, 79, 225, 101, 65, 92, 224, 1001,
             224, -147, 224, 4, 224, 1002, 223, 8, 223, 101, 4, 224, 224, 1, 223, 224,
             223, 1102, 16, 90, 225, 1102, 45, 44, 225, 1102, 92, 79, 225, 1002, 65,
             34, 224, 101, -476, 224, 224, 4, 224, 102, 8, 223, 223, 1001, 224, 5, 224,
             1, 224, 223, 223, 4, 223, 99, 0, 0, 0, 677, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             1105, 0, 99999, 1105, 227, 247, 1105, 1, 99999, 1005, 227, 99999,
             1005, 0, 256, 1105, 1, 99999, 1106, 227, 99999, 1106, 0, 265, 1105,
             1, 99999, 1006, 0, 99999, 1006, 227, 274, 1105, 1, 99999, 1105, 1, 280,
             1105, 1, 99999, 1, 225, 225, 225, 1101, 294, 0, 0, 105, 1, 0, 1105, 1, 99999,
             1106, 0, 300, 1105, 1, 99999, 1, 225, 225, 225, 1101, 314, 0, 0, 106, 0, 0, 1105,
             1, 99999, 107, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 329, 1001, 223, 1, 223,
             1007, 226, 226, 224, 102, 2, 223, 223, 1005, 224, 344, 101, 1, 223, 223, 1008, 226,
             226, 224, 102, 2, 223, 223, 1005, 224, 359, 1001, 223, 1, 223, 8, 226, 677, 224, 102,
             2, 223, 223, 1006, 224, 374, 101, 1, 223, 223, 1107, 226, 677, 224, 1002,
             223, 2, 223, 1006, 224, 389, 101, 1, 223, 223, 1108, 226, 677, 224, 102, 2,
             223, 223, 1005, 224, 404, 101, 1, 223, 223, 107, 677, 677, 224, 102, 2,
             223, 223, 1006, 224, 419, 1001, 223, 1, 223, 7, 677, 226, 224, 102, 2, 223,
             223, 1005, 224, 434, 101, 1, 223, 223, 1007, 677, 677, 224, 102, 2, 223, 223,
             1005, 224, 449, 1001, 223, 1, 223, 108, 226, 677, 224, 102, 2, 223, 223, 1005,
             224, 464, 1001, 223, 1, 223, 108, 226, 226, 224, 102, 2, 223, 223, 1006, 224,
             479, 101, 1, 223, 223, 107, 226, 677, 224, 102, 2, 223, 223, 1006, 224, 494, 1001,
             223, 1, 223, 7, 226, 226, 224, 1002, 223, 2, 223, 1006, 224, 509, 101, 1, 223, 223,
             1108, 677, 226, 224, 102, 2, 223, 223, 1005, 224, 524, 101, 1, 223, 223, 1107, 677,
             226, 224, 102, 2, 223, 223, 1005, 224, 539, 101, 1, 223, 223, 1008, 677, 226, 224, 102,
             2, 223, 223, 1005, 224, 554, 101, 1, 223, 223, 1008, 677, 677, 224, 1002,
             223, 2, 223, 1006, 224, 569, 101, 1, 223, 223, 1107, 677, 677, 224, 102, 2, 223,
             223, 1006, 224, 584, 1001, 223, 1, 223, 1108, 226, 226, 224, 1002, 223, 2, 223,
             1006, 224, 599, 101, 1, 223, 223, 7, 226, 677, 224, 102, 2, 223, 223, 1006, 224,
             614, 101, 1, 223, 223, 108, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 629,
             101, 1, 223, 223, 1007, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 644, 101,
             1, 223, 223, 8, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 659, 101, 1, 223,
             223, 8, 677, 226, 224, 102, 2, 223, 223, 1005, 224, 674, 101, 1, 223, 223, 4,
             223, 99, 226]

    # datas = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
    #          1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
    #          999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]

    opcodes = Opcodes(datas)
    opcodes.add_methods(1, add, 2, 1)
    opcodes.add_methods(2, multiply, 2, 1)
    opcodes.add_methods(3, inputt, 0, 1)
    opcodes.add_methods(4, outputt, 1, 0)
    opcodes.add_methods(5, jump_if_true, 2, 0)
    opcodes.add_methods(6, jump_if_false, 2, 0)
    opcodes.add_methods(7, less_than, 2, 1)
    opcodes.add_methods(8, equals, 2, 1)
    opcodes.add_methods(99, stop, 0, 0)
    # print(opcodes._codes)
    # opcodes.in_debug(True)
    opcodes.process()
