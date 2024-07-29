import random
import matplotlib.pyplot as plt
from prey import Prey
from predator import Predator
from config import GRID_SIZE, STEPS
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from tkinter import Label, Scale, Button

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
        self.initialize_simulation(100, 20, 50, 100, 0.1, 0.5, 0.01)
        self.setup_gui()

    def initialize_simulation(self, num_prey, num_predators, prey_energy, pred_energy, prey_energy_consumption, pred_energy_consumption, starvation_rate):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.preys = [Prey(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1), prey_energy) for _ in range(num_prey)]
        self.preds = [Predator(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1), pred_energy) for _ in
                      range(num_predators)]
        for prey in self.preys:
            self.grid[prey.x][prey.y] = 'Prey'
        for pred in self.preds:
            self.grid[pred.x][pred.y] = 'Predator'
        self.prey_energy_consumption = prey_energy_consumption
        self.pred_energy_consumption = pred_energy_consumption
        self.starvation_rate = starvation_rate

    def run_simulation(self):
        if self.ani is not None:
            self.ani.event_source.stop()  # Stop any existing animation
        self.ani = animation.FuncAnimation(self.fig, self.update, frames=STEPS, repeat=False)
        self.canvas.draw()

    def update(self, frame):
        for prey in self.preys:
            self.grid[prey.x][prey.y] = None
            prey.move(self.prey_energy_consumption)
            self.grid[prey.x][prey.y] = 'Prey'

        surviving_preds = []
        for pred in self.preds:
            self.grid[pred.x][pred.y] = None
            pred.move(self.grid, self.pred_energy_consumption)
            if self.grid[pred.x][pred.y] == 'Prey':
                pred.eat(self.prey_energy_consumption * 20)
                self.preys = [prey for prey in self.preys if prey.x != pred.x or prey.y != pred.y]
            else:
                pred.starve(self.starvation_rate)

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
                            command=lambda v: self.initialize_simulation(int(v), len(self.preds), 50, 100, 0.1, 0.5, 0.01))
        prey_slider.pack()

        Label(self.master, text="Number of Predators:").pack()
        predator_slider = Scale(self.master, from_=10, to=50, orient='horizontal',
                                command=lambda v: self.initialize_simulation(len(self.preys), int(v), 50, 100, 0.1, 0.5, 0.01))
        predator_slider.pack()

        run_button = Button(self.master, text="Run Simulation", command=self.run_simulation)
        run_button.pack()

        stop_button = Button(self.master, text="Stop Simulation", command=self.stop_simulation)
        stop_button.pack()
