"""
Where are they ?
"""
# standard imports
import re

# third party imports
import matplotlib.pyplot as plt

# local imports


class Planet:
    """ This is a planet """

    def __init__(self, x, y, z):
        self.position = [x, y, z]
        self.velocity = [0, 0, 0]
        # self.next_position = [0, 0, 0]
        # self.next_velocity = [0, 0, 0]
        self.positions = {"x": [0],
                          "y": [0],
                          "z": [0]}

    def __str__(self):
        return "Planet(x={}, y={}, z={}) vel:[x={}, y={}, z={}]".format(
            *(self.position + self.velocity))

    def __repr__(self):
        return "Planet(x={}, y={}, z={}) vel:[x={}, y={}, z={}]".format(
            *(self.position + self.velocity))

    def interact(self, other):
        """ this is how interact planets """
        # gravity
        for index, (axis, other_axis) in enumerate(zip(self.position, other.position)):
            if axis > other_axis:
                # self.next_position[index] = axis - 1
                self.velocity[index] -= 1
            elif axis < other_axis:
                # self.next_position[index] = axis + 1
                self.velocity[index] += 1

    def next(self):
        """ next second """
        # self.position = self.next_position.copy()
        # self.velocity = self.next_velocity.copy()
        # apply velocity
        for index, (pos, velocity) in enumerate(zip(self.position, self.velocity)):
            self.position[index] = pos + velocity
        # plot
        for axis, pos in zip(["x", "y", "z"], self.position):
            self.positions[axis].append(pos)

    def compute_energies(self):
        """  return potential energy and kinetic energy """
        return sum([abs(pot) for pot in self.position]), \
            sum([abs(kin) for kin in self.velocity])


def get_inputs():
    """ read input and return a list of planets """
    data = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>""".split("\n")
    with open("day12.input", "r") as fichier:
        data = fichier.readlines()
    data = [re.sub(r"[<>\n]", "", line) for line in data]

    planets = []
    for line in data:
        planets.append(Planet(*[int(x)
                                for x in re.sub(".=", "", line).split(",")]))
    for planet in planets:
        print(planet)
    print("")

    for interaction in range(1000+1):
        # print message ?
        if not interaction % 100:
            print("After {} step".format(interaction))
            for planet in planets:
                print(planet)
            pot = []
            kin = []
            for planet in planets:
                pot_, kin_ = planet.compute_energies()
                pot.append(pot_)
                kin.append(kin_)
            print("potential:", pot, " => ", sum(pot))
            print("kinetic  :", kin, " => ", sum(kin))
            print("Total    :", sum(
                [pot_*kin_ for pot_, kin_ in zip(pot, kin)]))
            print("")

        # normal run
        for planet in planets:
            for other in planets:
                if planet == other:
                    continue
                planet.interact(other)

        # go to next step
        for planet in planets:
            planet.next()

        # input("pause...")
        # for planet in planets:
        #     print(planet)

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    for planet in planets[1:]:
        ax.plot3D(planet.positions["x"],
                  planet.positions["y"],
                  planet.positions["z"])

    plt.show()


if __name__ == "__main__":
    get_inputs()
