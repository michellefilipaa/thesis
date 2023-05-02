from pyariadne import *
import builtins
import random
import numpy as np


class GlobalSearch:
    def __init__(self, payoff_function, lower_bound=-1, upper_bound=1):
        self.payoff_function = payoff_function
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def create_grid(self):
        # Define the range and spacing of the grid
        x_min, x_max = self.lower_bound, self.upper_bound
        y_min, y_max = self.lower_bound, self.upper_bound
        spacing = 0.1

        # Calculate the number of grid points in each dimension
        num_x = int((x_max - x_min) / spacing) + 1
        num_y = int((y_max - y_min) / spacing) + 1

        # Create a list of (x, y) coordinates
        grid_points = []
        for i in range(num_x):
            x = x_min + i * spacing
            for j in range(num_y):
                y = y_min + j * spacing
                grid_points.append(FloatDPBoundsVector([x_(float(x)), x_(float(y))], dp))

        return grid_points

    def calculate_payoff(self, grid_points):
        payoffs = []
        for point in grid_points:
            payoffs.append(self.payoff_function(point))

        return payoffs

    """
    |This method creates a payoff matrix from the generated grid.
    |"""
    def payoff_matrix(self, grid):
        matrix = self.calculate_payoff(grid)
        # Calculate the number of rows needed to fit all the elements
        num_rows = (len(grid) + 11) // 12

        # Create a list to hold the rows of the grid
        rows = []
        for i in range(num_rows):
            start = i * 12
            print(type(start))
            end = builtins.min((i + 1) * 12, len(grid))
            print(type(end))
            row = matrix[start:end] + [None] * (12 - (end - start))
            rows.append(row)

        # Append the rows list to the matrix list
        matrix.append(rows)

        return matrix

    @staticmethod
    def brute_force_nash_equilibrium(payoff_matrix):
        # payoff_matrix is a 2D list containing the payoffs for each player for all possible strategy combinations

        num_rows = len(payoff_matrix)
        num_cols = len(payoff_matrix[0])

        nash_equilibria = []

        for row in range(num_rows):
            for col in range(num_cols):
                is_nash_equilibrium = True

                # Check if this combination of strategies is a Nash Equilibrium for both players
                for i in range(num_rows):
                    if definitely(payoff_matrix[i][col] > payoff_matrix[row][col]):
                        is_nash_equilibrium = False
                        break

                for j in range(num_cols):
                    if definitely(payoff_matrix[row][j] > payoff_matrix[row][col]):
                        is_nash_equilibrium = False
                        break

                if is_nash_equilibrium:
                    nash_equilibria.append((row, col))

        return nash_equilibria

