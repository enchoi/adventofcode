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
K)L
K)YOU
I)SAN"""


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

    def set_parent(self, planet):
        """ who my mumy """
        self.parent = planet


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
            child.set_index(planet.index + 1)
            child.set_parent(planet)
            compute(child)

    compute(com)
    orbits = sum([planet.index for planet in planets.values()])
    print(f"Number of total orbits : {orbits}")
    return planets


def find_path_to_com(planet):
    """ find the path to COM """
    planet = planet.parent
    path = []
    while planet.name != "COM":
        path.append(planet.name)
        planet = planet.parent

    # add COM
    path.append(planet.name)
    return path[::-1]


def find_closer_parent(planet1, planet2):
    """ find the first relative """
    path1 = find_path_to_com(planet1)
    path2 = find_path_to_com(planet2)
    for plt1, plt2 in zip(path1, path2):
        if plt1 != plt2:
            break
        planet_joinction = plt1
    return planet_joinction
    # return (plt1.index - planet_joinction) + (plt2 - planet_joinction)


if __name__ == '__main__':
    # planets = main(test)
    with open("day6.input", "r") as fichier:
        data = fichier.read()
    planets = main(data)
    # print(total_orbits)
    # find_path_to_com(planets["YOU"])
    you = planets["YOU"]
    santa = planets["SAN"]

    joinction = find_closer_parent(you, santa)
    joinction = planets[joinction]

    distance = (you.index - joinction.index) + \
        (santa.index - joinction.index) - 2
    print(f"Orbits between you and Santa: {distance}")
