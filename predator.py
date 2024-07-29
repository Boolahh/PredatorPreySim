import random
from config import GRID_SIZE, VISION_RADIUS

class Predator:
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy

    def move(self, grid, energy_consumption):
        # Attempt to detect nearby prey and move towards it
        best_move = None
        min_dist = float('inf')
        for dx in range(-VISION_RADIUS, VISION_RADIUS + 1):
            for dy in range(-VISION_RADIUS, VISION_RADIUS + 1):
                nx, ny = (self.x + dx) % GRID_SIZE, (self.y + dy) % GRID_SIZE
                if grid[nx][ny] == 'Prey' and abs(dx) + abs(dy) < min_dist:
                    min_dist = abs(dx) + abs(dy)
                    best_move = (dx, dy)

        if best_move:
            self.x = (self.x + best_move[0]) % GRID_SIZE
            self.y = (self.y + best_move[1]) % GRID_SIZE
        else:
            self.x = (self.x + random.choice([-1, 0, 1])) % GRID_SIZE
            self.y = (self.y + random.choice([-1, 0, 1])) % GRID_SIZE
        self.energy -= energy_consumption

    def eat(self, prey_energy):
        self.energy += prey_energy

    def starve(self, starvation_rate):
        self.energy -= starvation_rate
