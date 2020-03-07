

def test1(code):
    # two digits at least are the same
    return len(set(code)) < 6


def test2(code):
    # digit never decrease
    for index in range(5):
        if code[index] > code[index + 1]:
            return False
    return True


def test3(code):
    # the two adjacent matching digits are not part of a larger group of
    # matching digits
    for char in set(code):
        if code.count(char) == 2:
            return True
    return False


if __name__ == "__main__":
    length = []
    for code in range(138241, 674034):
        code = str(code)
        if test1(code) and test2(code) and test3(code):
            length.append(int(code))
    print(len(length))
