import random
import tkinter as tk
import matplotlib.pyplot as plt
from prey import Prey
from predator import Predator
from config import GRID_SIZE, STEPS
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from tkinter import Label, Scale, Button, Frame


class Simulation:
    def __init__(self, master):
        self.master = master
        self.master.geometry('1600x900')

        # Setup control frame
        control_frame = Frame(self.master, width=300)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Add controls
        self.setup_controls(control_frame)

        # Setup canvas frame
        canvas_frame = Frame(self.master)
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create figure and canvas
        self.fig, (self.ax, self.ax2) = plt.subplots(2, 1, figsize=(12, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=canvas_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.preys = []
        self.preds = []
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.ani = None  # Animation object
        self.prey_data = []
        self.pred_data = []
        self.initialize_simulation(100, 20, 50, 100, 0.1, 0.5, 0.01, 0.05, 0.05)

    def initialize_simulation(self, num_prey, num_predators, prey_energy, pred_energy, prey_energy_consumption,
                              pred_energy_consumption, starvation_rate, prey_reproduction_prob, pred_reproduction_prob):
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.preys = [Prey(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1), prey_energy) for _ in
                      range(num_prey)]
        self.preds = [Predator(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1), pred_energy) for _ in
                      range(num_predators)]
        for prey in self.preys:
            self.grid[prey.x][prey.y] = 'Prey'
        for pred in self.preds:
            self.grid[pred.x][pred.y] = 'Predator'
        self.prey_energy_consumption = prey_energy_consumption
        self.pred_energy_consumption = pred_energy_consumption
        self.starvation_rate = starvation_rate
        self.prey_reproduction_prob = prey_reproduction_prob
        self.pred_reproduction_prob = pred_reproduction_prob

    def run_simulation(self):
        if self.ani is not None:
            self.ani.event_source.stop()  # Stop any existing animation
        self.ani = animation.FuncAnimation(self.fig, self.update, frames=STEPS, repeat=False)
        self.canvas.draw()

    def update(self, frame):
        weather_effect = random.choice([0, -0.1, 0.1])  # Simplified weather effect
        disease_effect = random.choice([0, -0.05]) if random.random() < 0.1 else 0  # Simplified disease effect

        new_preys = []
        for prey in self.preys:
            self.grid[prey.x][prey.y] = None
            prey.move(self.prey_energy_consumption + weather_effect + disease_effect)
            if prey.energy > 0:
                self.grid[prey.x][prey.y] = 'Prey'
                new_preys.append(prey)
                new_prey = prey.reproduce(self.prey_reproduction_prob)
                if new_prey:
                    new_preys.append(new_prey)
                    self.grid[new_prey.x][new_prey.y] = 'Prey'

        new_preds = []
        for pred in self.preds:
            self.grid[pred.x][pred.y] = None
            pred.move(self.grid, self.pred_energy_consumption + weather_effect + disease_effect)
            if self.grid[pred.x][pred.y] == 'Prey':
                pred.eat(self.prey_energy_consumption * 20)
                self.preys = [prey for prey in self.preys if prey.x != pred.x or prey.y != pred.y]
            else:
                pred.starve(self.starvation_rate + disease_effect)

            if pred.energy > 0:
                new_preds.append(pred)
                self.grid[pred.x][pred.y] = 'Predator'
                new_pred = pred.reproduce(self.pred_reproduction_prob)
                if new_pred:
                    new_preds.append(new_pred)
                    self.grid[new_pred.x][new_pred.y] = 'Predator'

        self.preys = new_preys
        self.preds = new_preds
        self.ax.clear()
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if self.grid[x][y] == 'Prey':
                    self.ax.plot(x, y, 'go')
                elif self.grid[x][y] == 'Predator':
                    self.ax.plot(x, y, 'ro')

        self.prey_data.append(len(self.preys))
        self.pred_data.append(len(self.preds))

        self.ax2.clear()
        self.ax2.plot(self.prey_data, label='Prey')
        self.ax2.plot(self.pred_data, label='Predator')
        self.ax2.legend()
        self.canvas.draw()

    def stop_simulation(self):
        if self.ani is not None:
            self.ani.event_source.stop()  # Properly stop the animation
            self.ax.clear()
            self.ax2.clear()
            self.canvas.draw()

    def setup_controls(self, control_frame):
        Label(control_frame, text="Initial Number of Prey:").pack()
        prey_slider = Scale(control_frame, from_=50, to=200, orient='horizontal',
                            command=lambda v: self.initialize_simulation(int(v), len(self.preds), 50, 100,
                                                                         self.prey_energy_consumption,
                                                                         self.pred_energy_consumption,
                                                                         self.starvation_rate,
                                                                         self.prey_reproduction_prob,
                                                                         self.pred_reproduction_prob))
        prey_slider.pack()

        Label(control_frame, text="Initial Number of Predators:").pack()
        predator_slider = Scale(control_frame, from_=10, to=50, orient='horizontal',
                                command=lambda v: self.initialize_simulation(len(self.preys), int(v), 50, 100,
                                                                             self.prey_energy_consumption,
                                                                             self.pred_energy_consumption,
                                                                             self.starvation_rate,
                                                                             self.prey_reproduction_prob,
                                                                             self.pred_reproduction_prob))
        predator_slider.pack()

        Label(control_frame, text="Prey Energy:").pack()
        prey_energy_slider = Scale(control_frame, from_=10, to=100, orient='horizontal',
                                   command=lambda v: self.initialize_simulation(len(self.preys), len(self.preds),
                                                                                int(v), self.preds[
                                                                                    0].energy if self.preds else 100,
                                                                                self.prey_energy_consumption,
                                                                                self.pred_energy_consumption,
                                                                                self.starvation_rate,
                                                                                self.prey_reproduction_prob,
                                                                                self.pred_reproduction_prob))
        prey_energy_slider.pack()

        Label(control_frame, text="Predator Energy:").pack()
        predator_energy_slider = Scale(control_frame, from_=50, to=200, orient='horizontal',
                                       command=lambda v: self.initialize_simulation(len(self.preys), len(self.preds),
                                                                                    self.preys[
                                                                                        0].energy if self.preys else 50,
                                                                                    int(v),
                                                                                    self.prey_energy_consumption,
                                                                                    self.pred_energy_consumption,
                                                                                    self.starvation_rate,
                                                                                    self.prey_reproduction_prob,
                                                                                    self.pred_reproduction_prob))
        predator_energy_slider.pack()

        Label(control_frame, text="Prey Energy Consumption:").pack()
        prey_energy_consumption_slider = Scale(control_frame, from_=0.01, to=1.0, resolution=0.01, orient='horizontal',
                                               command=lambda v: self.initialize_simulation(len(self.preys),
                                                                                            len(self.preds), self.preys[
                                                                                                0].energy if self.preys else 50,
                                                                                            self.preds[
                                                                                                0].energy if self.preds else 100,
                                                                                            float(v),
                                                                                            self.pred_energy_consumption,
                                                                                            self.starvation_rate,
                                                                                            self.prey_reproduction_prob,
                                                                                            self.pred_reproduction_prob))
        prey_energy_consumption_slider.pack()

        Label(control_frame, text="Predator Energy Consumption:").pack()
        predator_energy_consumption_slider = Scale(control_frame, from_=0.1, to=2.0, resolution=0.1,
                                                   orient='horizontal',
                                                   command=lambda v: self.initialize_simulation(len(self.preys),
                                                                                                len(self.preds),
                                                                                                self.preys[
                                                                                                    0].energy if self.preys else 50,
                                                                                                self.preds[
                                                                                                    0].energy if self.preds else 100,
                                                                                                self.prey_energy_consumption,
                                                                                                float(v),
                                                                                                self.starvation_rate,
                                                                                                self.prey_reproduction_prob,
                                                                                                self.pred_reproduction_prob))
        predator_energy_consumption_slider.pack()

        Label(control_frame, text="Starvation Rate:").pack()
        starvation_rate_slider = Scale(control_frame, from_=0.01, to=1.0, resolution=0.01, orient='horizontal',
                                       command=lambda v: self.initialize_simulation(len(self.preys), len(self.preds),
                                                                                    self.preys[
                                                                                        0].energy if self.preys else 50,
                                                                                    self.preds[
                                                                                        0].energy if self.preds else 100,
                                                                                    self.prey_energy_consumption,
                                                                                    self.pred_energy_consumption,
                                                                                    float(v),
                                                                                    self.prey_reproduction_prob,
                                                                                    self.pred_reproduction_prob))
        starvation_rate_slider.pack()

        Label(control_frame, text="Prey Reproduction Probability:").pack()
        prey_reproduction_prob_slider = Scale(control_frame, from_=0.01, to=0.5, resolution=0.01, orient='horizontal',
                                              command=lambda v: self.initialize_simulation(len(self.preys),
                                                                                           len(self.preds), self.preys[
                                                                                               0].energy if self.preys else 50,
                                                                                           self.preds[
                                                                                               0].energy if self.preds else 100,
                                                                                           self.prey_energy_consumption,
                                                                                           self.pred_energy_consumption,
                                                                                           self.starvation_rate,
                                                                                           float(v),
                                                                                           self.pred_reproduction_prob))
        prey_reproduction_prob_slider.pack()

        Label(control_frame, text="Predator Reproduction Probability:").pack()
        predator_reproduction_prob_slider = Scale(control_frame, from_=0.01, to=0.5, resolution=0.01,
                                                  orient='horizontal',
                                                  command=lambda v: self.initialize_simulation(len(self.preys),
                                                                                               len(self.preds),
                                                                                               self.preys[
                                                                                                   0].energy if self.preys else 50,
                                                                                               self.preds[
                                                                                                   0].energy if self.preds else 100,
                                                                                               self.prey_energy_consumption,
                                                                                               self.pred_energy_consumption,
                                                                                               self.starvation_rate,
                                                                                               self.prey_reproduction_prob,
                                                                                               float(v)))
        predator_reproduction_prob_slider.pack()

        run_button = Button(control_frame, text="Run Simulation", command=self.run_simulation)
        run_button.pack()

        stop_button = Button(control_frame, text="Stop Simulation", command=self.stop_simulation)
        stop_button.pack()
