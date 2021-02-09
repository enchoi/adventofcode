import numpy as np
from itertools import chain


class Elves_Image:
    def __init__(self, width, height, data):
        self.layers = []
        self.data = data
        self.width = width
        self.height = height

        # compute layers
        self.compute()

    def compute(self):
        """ split data into multiple layers """
        size = self.height * self.width
        layers = [self.data[size*x:(x+1)*size]
                  for x in range(int(len(self.data)/size))]
        self.layers = [np.resize(list(layer), (self.height, self.width))
                       for layer in layers]

    def find(self, condition="fewest", number="0"):
        """ find a layer """
        if condition == "fewest":
            rev = False
        elif condition == "most":
            rev = True
        if isinstance(number, int):
            number = str(number)

        # strings = [self._to_string(layer), for layer in layers]
        layer = sorted(self.layers,
                       key=lambda x:
                       self.to_string(x).count(number), reverse=rev)[0]

        return layer

    @staticmethod
    def to_string(layer):
        """ transform a layer into string """
        return "".join(chain.from_iterable(layer.tolist()))

    def stack_layer(self):
        """ Stack all layers """
        layers = [list(chain.from_iterable(layer)) for layer in self.layers]
        transparent = "2"
        image = layers[0]
        for layer in layers:
            for index, (pixel_i, pixel_l) in enumerate(zip(image, layer)):
                if pixel_i == transparent:
                    image[index] = pixel_l

        # applay color
        white = chr(9608)
        black = " "
        for index, pixel in enumerate(image):
            image[index] = white if pixel == "1" else black
        # print the image
        for line in np.resize(image, (self.height, self.width)):
            print("".join(line))

        return image


def main():
    """ the main test """
    with open("day8.input", "r") as fichier:
        data = fichier.read()

    image = Elves_Image(25, 6, data)
    layer = image.find()
    layer_data = image.to_string(layer)
    ones = layer_data.count("1")
    twos = layer_data.count("2")
    print(f"1: {ones}")
    print(f"2: {twos}")
    print(f"multiplication: {ones * twos}")
    return image


def main2(image):
    """ the main 2 """
    image.stack_layer()


if __name__ == '__main__':
    image = main()
    main2(image)
