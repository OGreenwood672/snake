import random

class fruit:
    def __init__(self, display_width, display_height, size):
        self.display_width = display_width
        self.display_height = display_height
        self.size = size
        self.spot()

    def spot(self):
        self.fruitX = int(round(random.randint(0, self.display_width * 0.99) / self.size) * self.size)
        self.fruitY = int(round(random.randint(0, self.display_height * 0.99) / self.size) * self.size)

