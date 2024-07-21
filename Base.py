import tkinter as tk
from tkinter import Scale, Label, Button
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import random

# Constants
GRID_SIZE = 50
STEPS = 300
VISION_RADIUS = 5  # New constant for predator vision


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
        self.energy = 50  # Increased initial energy for better survival

    def move(self, grid):
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
        self.energy -= 0.5

    def eat(self):
        self.energy += 20

    def starve(self):
        self.energy -= 1


class Simulation:
    def __init__(self, master):
        self.master = master
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)  # Embed figure in the Tkinter window
        self.canvas.get_tk_widget().pack()
        self.preys = []
        self.preds = []
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.ani = None  # Animation object
        self.initialize_simulation(100, 20)
        self.setup_gui()

    def initialize_simulation(self, num_prey, num_predators):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.preys = [Prey(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)) for _ in range(num_prey)]
        self.preds = [Predator(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)) for _ in
                      range(num_predators)]
        for prey in self.preys:
            self.grid[prey.x][prey.y] = 'Prey'
        for pred in self.preds:
            self.grid[pred.x][pred.y] = 'Predator'

    def run_simulation(self):
        if self.ani is not None:
            self.ani.event_source.stop()  # Stop any existing animation
        self.ani = animation.FuncAnimation(self.fig, self.update, frames=STEPS, repeat=False)
        self.canvas.draw()

    def update(self, frame):
        for prey in self.preys:
            self.grid[prey.x][prey.y] = None
            prey.move()
            self.grid[prey.x][prey.y] = 'Prey'

        surviving_preds = []
        for pred in self.preds:
            self.grid[pred.x][pred.y] = None
            pred.move(self.grid)
            if self.grid[pred.x][pred.y] == 'Prey':
                pred.eat()
                self.preys = [prey for prey in self.preys if prey.x != pred.x or prey.y != pred.y]
            else:
                pred.starve()

            if pred.energy > 0:
                surviving_preds.append(pred)
                self.grid[pred.x][pred.y] = 'Predator'

        self.preds = surviving_preds
        self.ax.clear()
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if self.grid[x][y] == 'Prey':
                    self.ax.plot(x, y, 'go')
                elif self.grid[x][y] == 'Predator':
                    self.ax.plot(x, y, 'ro')

    def stop_simulation(self):
        if self.ani is not None:
            self.ani.event_source.stop()  # Properly stop the animation
            self.ax.clear()
            self.canvas.draw()

    def setup_gui(self):
        Label(self.master, text="Number of Prey:").pack()
        prey_slider = Scale(self.master, from_=50, to=200, orient='horizontal',
                            command=lambda v: self.initialize_simulation(int(v), len(self.preds)))
        prey_slider.pack()

        Label(self.master, text="Number of Predators:").pack()
        predator_slider = Scale(self.master, from_=10, to=50, orient='horizontal',
                                command=lambda v: self.initialize_simulation(len(self.preys), int(v)))
        predator_slider.pack()

        run_button = Button(self.master, text="Run Simulation", command=self.run_simulation)
        run_button.pack()

        stop_button = Button(self.master, text="Stop Simulation", command=self.stop_simulation)
        stop_button.pack()


# Main execution
root = tk.Tk()
root.title("Predator-Prey Simulation Controls")
simulation = Simulation(root)
root.mainloop()
