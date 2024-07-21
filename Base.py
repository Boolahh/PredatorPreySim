import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Constants
GRID_SIZE = 20
NUM_PREY = 50
NUM_PREDATORS = 20
STEPS = 100

# Classes for Prey and Predator
class Prey:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        self.x = (self.x + random.choice([-1, 0, 1])) % GRID_SIZE
        self.y = (self.y + random.choice([-1, 0, 1])) % GRID_SIZE

class Predator:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energy = 10  # Increased initial energy from 5 to 10

    def move(self):
        self.x = (self.x + random.choice([-1, 0, 1])) % GRID_SIZE
        self.y = (self.y + random.choice([-1, 0, 1])) % GRID_SIZE
        self.energy -= 0.5  # Decreased energy loss per move from 1 to 0.5

    def eat(self):
        self.energy += 5

    def starve(self):
        self.energy -= 1  # Constant starve amount

# Initialize the grid
grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Place prey randomly on the grid
prey_list = []
for _ in range(NUM_PREY):
    x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
    prey = Prey(x, y)
    prey_list.append(prey)
    grid[x][y] = 'Prey'

# Place predators randomly on the grid
predator_list = []
for _ in range(NUM_PREDATORS):
    x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
    predator = Predator(x, y)
    predator_list.append(predator)
    grid[x][y] = 'Predator'

# Simulation loop
fig, ax = plt.subplots()

def update(frame):
    global prey_list, predator_list, grid

    ax.clear()

    # Move prey
    for prey in prey_list:
        grid[prey.x][prey.y] = None
        prey.move()
        grid[prey.x][prey.y] = 'Prey'

    # Move predators
    for predator in predator_list:
        grid[predator.x][predator.y] = None
        predator.move()

        if grid[predator.x][predator.y] == 'Prey':
            predator.eat()
            prey_list = [prey for prey in prey_list if prey.x != predator.x or prey.y != predator.y]
        else:
            predator.starve()

        if predator.energy > 0:
            grid[predator.x][predator.y] = 'Predator'
        else:
            predator_list.remove(predator)

    # Draw the grid
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x][y] == 'Prey':
                ax.plot(x, y, 'go')  # Green for prey
            elif grid[x][y] == 'Predator':
                ax.plot(x, y, 'ro')  # Red for predators

ani = animation.FuncAnimation(fig, update, frames=STEPS, repeat=False)
plt.show()
