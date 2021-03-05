"""
day 14
"""


class Bank:
    """ you can get chemical here """

    def __init__(self, reactions):
        self.reactions = reactions
        self._ore = 0
        self.safe = {}

    def get(self, typ, number):
        """ get chemical """
        while self.safe.get(typ, 0) < number:
            self.create(typ)
        # if self.safe.get(typ, 0) >= number:
        self.safe[typ] -= number
        # return

    def create(self, typ):
        """ create chemical """
        if typ == "ORE":
            self._ore += 1
            self.safe[typ] = self.safe.get(typ, 0) + 1
            return
        times, compo = self.reactions[typ]
        for chem, num in compo.items():
            self.get(chem, num)

        self.safe[typ] = self.safe.get(typ, 0) + times

    def get_the_check(self):
        """ return the number of ore needed to compute what is asked """
        return self._ore


def get_data():
    """ read the file """
    with open("day14.input", "r") as fichier:
        return fichier.readlines()


def compute_data(data):
    """ shop know what it's needed to get materials """
    reactions = {}
    for line in data:
        start,  end = line.split(" => ")
        number, typ_ = end.strip().split(" ")
        elem_needed = {}
        for elem in start.split(", "):
            nb_, typ = elem.strip().split(" ")
            nb_ = int(nb_)
            typ = typ.strip()
            elem_needed[typ] = nb_
        reactions[typ_] = (int(number), elem_needed)
    return reactions


if __name__ == "__main__":
    data = get_data()
    reactions = compute_data(data)
    bank = Bank(reactions)
    bank.get("FUEL", 1)
    print(bank.get_the_check())
