test = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""


class Planet:
    def __init__(self, name):
        self.children = {}
        self.parent = None
        self.name = name
        self.index = 0

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def set_index(self, index):
        """ set my index """
        self.index = index

    def add_child(self, planet):
        """ Add planet in obit """
        self.children[planet.name] = planet


def main(entry):
    # create planets
    links = entry.split("\n")
    planets = {name: Planet(name) for link in links
               for name in link.split(")")}

    for center, orbit in [link.split(")") for link in links]:
        planets[center].add_child(planets[orbit])

    # compute number of orbits
    # first is CenterOfMass
    com = planets["COM"]

    def compute(planet):
        for _, child in planet.children.items():
            child.set_index(planet.index+1)
            compute(child)

    compute(com)
    orbits = sum([planet.index for planet in planets.values()])
    return orbits


if __name__ == '__main__':
    # total_orbits = main(test)
    with open("day6.input", "r") as fichier:
        data = fichier.read()
    total_orbits = main(data)
    print(total_orbits)
