import tkinter as tk
from tkinter import Scale, Label, Button, Toplevel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import random

# Constants
GRID_SIZE = 20
STEPS = 100
VISION_RADIUS = 3

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
        self.energy = 10

    def move(self, grid):
        found_prey = None
        for dx in range(-VISION_RADIUS, VISION_RADIUS + 1):
            for dy in range(-VISION_RADIUS, VISION_RADIUS + 1):
                nx, ny = (self.x + dx) % GRID_SIZE, (self.y + dy) % GRID_SIZE
                if grid[nx][ny] == 'Prey':
                    found_prey = (dx, dy)
                    break
            if found_prey:
                break
        if found_prey:
            self.x = (self.x + found_prey[0]) % GRID_SIZE
            self.y = (self.y + found_prey[1]) % GRID_SIZE
        else:
            self.x = (self.x + random.choice([-1, 0, 1])) % GRID_SIZE
            self.y = (self.y + random.choice([-1, 0, 1])) % GRID_SIZE
        self.energy -= 0.5

    def eat(self):
        self.energy += 5

    def starve(self):
        self.energy -= 1

# Tkinter main window setup
root = tk.Tk()
root.title("Predator-Prey Simulation Controls")

# Variables for dynamic updates
num_prey = tk.IntVar(value=50)
num_predators = tk.IntVar(value=20)

Label(root, text="Number of Prey:").pack()
prey_scale = Scale(root, from_=10, to=100, orient='horizontal', variable=num_prey)
prey_scale.pack()

Label(root, text="Number of Predators:").pack()
predator_scale = Scale(root, from_=5, to=50, orient='horizontal', variable=num_predators)
predator_scale.pack()

# Separate window for the plot to keep GUI clean
plot_window = Toplevel(root)
plot_window.title("Simulation Plot")

# Setting up the figure and embedding it in the Tkinter window
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=plot_window)  # Embedding the plot
canvas.draw()
canvas.get_tk_widget().pack()

# Function to start the simulation
def start_simulation():
    prey_list = [Prey(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)) for _ in range(num_prey.get())]
    predator_list = [Predator(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)) for _ in range(num_predators.get())]
    grid = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def animate(frame):
        ax.clear()
        for prey in prey_list:
            prey.move()
            ax.plot(prey.x, prey.y, 'go')
        for predator in predator_list:
            predator.move(grid)
            if grid[predator.x][predator.y] == 'Prey':
                predator.eat()
            else:
                predator.starve()
            if predator.energy > 0:
                ax.plot(predator.x, predator.y, 'ro')
            else:
                predator_list.remove(predator)
        return ax,

    ani = animation.FuncAnimation(fig, animate, frames=STEPS, repeat=False)
    canvas.draw()

start_button = Button(root, text="Start Simulation", command=start_simulation)
start_button.pack()

root.mainloop()


