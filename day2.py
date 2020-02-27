dic_func = {
    1: lambda a, b: a+b,
    2: lambda a, b: a*b
}


def opcode(opcodes):
    index = 0
    cop = opcodes.copy()
    while cop[index] != 99:
        operation = cop[index]
        index_1 = cop[index + 1]
        index_2 = cop[index + 2]
        index_result = cop[index + 3]
        cop[index_result] = dic_func[operation](cop[index_1], cop[index_2])
        index += 4
    return cop


assert opcode([1, 0, 0, 0, 99]) == [2, 0, 0, 0, 99]
assert opcode([2, 3, 0, 3, 99]) == [2, 3, 0, 6, 99]
assert opcode([2, 4, 4, 5, 99, 0]) == [2, 4, 4, 5, 99, 9801]
assert opcode([1, 1, 1, 4, 99, 5, 6, 0, 99]) == [30, 1, 1, 4, 2, 5, 6, 0, 99]


data = [1, 0, 0, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 1, 9, 19, 1, 13, 19, 23, 2, 23, 9, 27, 1, 6, 27, 31, 2, 10, 31, 35, 1, 6, 35, 39, 2, 9, 39, 43, 1, 5, 43, 47, 2, 47, 13, 51, 2, 51, 10, 55, 1, 55, 5, 59, 1, 59, 9, 63, 1, 63,
        9, 67, 2, 6, 67, 71, 1, 5, 71, 75, 1, 75, 6, 79, 1, 6, 79, 83, 1, 83, 9, 87, 2, 87, 10, 91, 2, 91, 10, 95, 1, 95, 5, 99, 1, 99, 13, 103, 2, 103, 9, 107, 1, 6, 107, 111, 1, 111, 5, 115, 1, 115, 2, 119, 1, 5, 119, 0, 99, 2, 0, 14, 0]
