import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


class GUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Function Plotter")

        # create GUI components
        self.label = tk.Label(self.master, text="Enter the payoff functions:")
        self.label.pack(side="top")

        self.entry = tk.Entry(self.master, width=50)
        self.entry.pack(side="top")

        self.button = tk.Button(self.master, text="Plot", command=self.plot)
        self.button.pack(side="top")

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.plot_canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.plot_canvas.get_tk_widget().pack(side="bottom")

    def plot(self):
        # clear previous plot
        self.figure.clear()

        # get user input
        function = self.entry.get()

        # create data for plot
        x = np.linspace(-10, 10, 1000)
        y = eval(function)

        # create subplot and plot data
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)

        # redraw canvas
        self.plot_canvas.draw()


# create main window and run app
root = tk.Tk()
app = GUI(master=root)
app.mainloop()
