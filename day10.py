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
        return ((int(col/gcd), int(row/gcd)), norm)

    def compute_los(self, position, debug=False, get_directions=False):
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
        if get_directions:
            return len(direction), direction
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

    def apply_raygun(self, position, print_map=False):
        """ use the ray gun at the good position """
        # get the list of all astéroid visible
        _, asteroids = self.compute_los(position, get_directions=True)

        # sort clockwise
        # sorted_direction = sorted(asteroids.keys(), key=self.sort_direction, reverse=True)
        destroyed_asteroid = []
        # destroy them all
        while asteroids:
            for direction in sorted(asteroids.keys(), key=self.sort_direction, reverse=True):
                # destroy the first asteroïd in sight

                for first_in_sight in sorted(asteroids[direction],
                                             key=lambda x: x[0],
                                             reverse=False):
                    destroyed_asteroid.append(
                        asteroids[direction].pop(
                            asteroids[direction].index(first_in_sight)))
                    break
                if not asteroids[direction]:
                    asteroids.pop(direction)

        if print_map:
            h = len(self._map)
            w = len(self._map[0])
            positions = [x[1] for x in destroyed_asteroid]
            for y in range(h):
                for x in range(w):
                    if self._map[y][x] == ".":
                        print("  .  ", end="")
                    else:
                        try:
                            print(f"{positions.index((x,y))+1: ^#5}", end="")
                        except ValueError:
                            # It's me !
                            print(f"  X  ", end="")
                print("")

        return destroyed_asteroid

    @staticmethod
    def sort_direction(direction):
        """ sort direction clockwise starting from "UP" """
        # get the angle but if y>0 and x<0 tweak the result
        direction = (direction[0], -direction[1])
        angle = math.atan2(*direction[::-1])
        if direction[1] >= 0 and direction[0] < 0:
            angle = -math.pi-(math.pi-angle)
        return angle


def main():
    map_ = """.#..#
.....
#####
....#
...##"""
    with open("day10.input", "r") as fichier:
        map_ = fichier.read()
    station = MonitorStation()
    station.set_map(map_)
    spot, in_sight = station.find_spot()
    print(spot, in_sight)
    destroyed_asteroid = station.apply_raygun(spot, True)
    # select 200th destroyed asteroid.
    winner = destroyed_asteroid[200-1]
    position = winner[1]
    print(position[0]*100 + position[1])
    return station


""" TEST:
heure = {
1:(4716158501352293, 4503599627370496),
2:(4716158501352293, 9007199254740992),
3:(0,1),
4:(-4716158501352293, 9007199254740992),
5:(-4716158501352293, 4503599627370496),
6:(-1,0),
7:(-4716158501352293, -4503599627370496),
8:(-4716158501352293, -9007199254740992),
9:(0,-1),
10:(4716158501352293, -9007199254740992),
11:(4716158501352293, -4503599627370496),
12:(1,0),
}
sorted(heure, key=lambda x: sort_direction(heure[x]), reverse=True)

Out[23]: [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
"""

if __name__ == '__main__':
    main()
