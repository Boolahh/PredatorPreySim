import tkinter as tk
from tkinter import Scale, Label, Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from simulation import Simulation

# Main execution
root = tk.Tk()
root.title("Predator-Prey Simulation Controls")
simulation = Simulation(root)
root.mainloop()

