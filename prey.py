import random
from config import GRID_SIZE

class Prey:
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy

    def move(self, energy_consumption):
        self.x = (self.x + random.choice([-1, 0, 1])) % GRID_SIZE
        self.y = (self.y + random.choice([-1, 0, 1])) % GRID_SIZE
        self.energy -= energy_consumption

    def reproduce(self, reproduction_prob):
        if random.random() < reproduction_prob:
            return Prey(self.x, self.y, self.energy)
        return None
