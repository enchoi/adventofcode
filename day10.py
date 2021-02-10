"""
Help the elves to seek the good place.
"""
import math

class MonitorStation:
    """ the new monitor station for elves """

    def __init__(self):
        self._map = None

    def set_map(self, new_map):
        """ Set a new map """
        self._map = new_map.split("\n")

    @staticmethod
    def direction_norm(vect):
        """ get the direction and the norm of a vector """
        norm = (vect[0]**2 + vect[1]**2)**0.5
        # norm = math.sqrt(pow(vect[1], 2) + pow(vect[1], 2))
        # return (vect[0] / norm, vect[1] / norm), norm
        col, row = vect
        gcd = math.gcd(*vect)
        return ((int(col)/gcd, int(row)/gcd), norm)

    def compute_los(self, position, debug=False):
        """ compute the line of sight for the given position """
        if self._map is None:
            raise AttributeError("Map not set")

        if self._map[position[1]][position[0]] == ".":
            # no asteroid here
            return None

        direction = {}
        rows = len(self._map)
        columns = len(self._map[0])
        for row in range(rows):
            for col in range(columns):
                # no asteroid, continue to search
                if self._map[row][col] == ".":
                    continue
                if (col, row) == position:
                    continue

                dire, norm = self.direction_norm((col - position[0],
                                                  row - position[1]))
                direction.setdefault(dire, []).append((norm, (col, row)))

        # who is behind who
        if debug:
            for dire, values in direction.items():
                print(f"{dire} :")
                for index, (norm, pos) in enumerate(values):
                    print(f"\t{index}: position {pos} | norm {norm}")

        # return number of asteroid in sight
        return len(direction)

    def find_spot(self, to_print=False):
        """ print the number of found asteroid depending the position """
        rows = len(self._map)
        columns = len(self._map[0])
        location = {}
        for row in range(rows):
            for col in range(columns):
                nb_asteroid = self.compute_los((col, row))
                if nb_asteroid is not None:
                    location[(col, row)] = nb_asteroid

                if to_print:
                    if self._map[row][col] == ".":
                        print("  .  ", end='')
                    else:
                        print(f"{nb_asteroid: ^#5}", end="")
            if to_print:
                print("")

        spot = sorted(location.keys(), key=lambda x: location[x])[-1]
        return spot, location[spot]


def main():
    map_ = """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""
    with open("day10.input", "r") as fichier:
        map_ = fichier.read()
    station = MonitorStation()
    station.set_map(map_)
    print(station.find_spot())


if __name__ == '__main__':
    main()
