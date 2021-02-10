import day5


def main():
    """ the main """
    with open("day9.input", "r") as fichier:
        instructions = [int(x) for x in fichier.read().split(",")]

    opcode = day5.get_int_code_configured()
    opcode.set_codes(instructions)
    opcode.process()
    del opcode


if __name__ == '__main__':
    main()
