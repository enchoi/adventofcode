"""
Where are they ?

Part 2:
I don't figure it out myself... i'm to dumb

each axis rotation are separate.
To find the solution, we need to find each rotation axis length and
find the least commun multiple numpy.lcm of each circle length
"""
# standard imports
import re
import math

# third party imports

# local imports


def lcm(a, b):
    """ get the lcm """
    if a and b:
        return int(abs(a * b) / math.gcd(a, b))
    return 0


class Planet:
    """ This is a planet """

    def __init__(self, x, y, z):
        self.position = [x, y, z]
        self.velocity = [0, 0, 0]

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
                self.velocity[index] -= 1
            elif axis < other_axis:
                self.velocity[index] += 1

    def next(self):
        """ next second """
        # apply velocity
        for index, (pos, velocity) in enumerate(zip(self.position, self.velocity)):
            self.position[index] = pos + velocity

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

    # for interaction in range(1000+1):
    x_states = set()
    y_states = set()
    z_states = set()
    try:
        while True:
            # normal run
            for planet in planets:
                for other in planets:
                    if planet == other:
                        continue
                    planet.interact(other)

            # go to next step
            for planet in planets:
                planet.next()

            # save
            x_state = tuple([(planet.position[0], planet.velocity[0])
                             for planet in planets])
            y_state = tuple([(planet.position[1], planet.velocity[1])
                             for planet in planets])
            z_state = tuple([(planet.position[2], planet.velocity[2])
                             for planet in planets])
            if all([state in states for state, states in zip([x_state, y_state, z_state],
                                                             [x_states, y_states, z_states])]):
                break
            x_states.add(x_state)
            y_states.add(y_state)
            z_states.add(z_state)
        # find the lcm of each length of circle
        print(lcm(lcm(len(x_states), len(y_states)), len(z_states)))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    get_inputs()
