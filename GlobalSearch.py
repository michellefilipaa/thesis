from pyariadne import *
import numpy as np
from LocalConvergence import LocalConvergence


class GlobalSearch:
    def __init__(self, payoff_function, lower_bound=-1, upper_bound=1):
        self.payoff_function = payoff_function
        # PC: Suggest using a Box with lower and upper bounds for each player
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    """
    |This method creates a grid of strategies for each player at intervals of 'spacing'.
    |These will be used to find potential approximate Nash equilibria.
    """
    def create_grid(self, spacing=0.1):
        # Define the range and spacing of the grid
        x_min, x_max = self.lower_bound, self.upper_bound
        y_min, y_max = self.lower_bound, self.upper_bound

        num_x = round((x_max - x_min) / spacing) + 1
        num_y = round((y_max - y_min) / spacing) + 1

        grid_points = np.zeros((num_x, num_y), dtype=object)  # Create a list of (x, y) coordinates
        payoff_matrix = np.zeros((num_x, num_y), dtype=object)  # Corresponding payoff value at coordinate

        for i in range(num_x):
            x = x_min + i * spacing
            for j in range(num_y):
                y = y_min + j * spacing
                point = FloatDPBoundsVector([x_(x), x_(y)], dp)
                grid_points[i, j] = point
                payoff_matrix[i, j] = self.payoff_function(point)

        return grid_points, payoff_matrix

    """
    |This method takes in one row of the payoff matrix. Each row represents the payoffs for p0 and p1 given 
    |a fixed strategy for p0 and different strategies for p1 in each index.
    |The method will search for the strategy of p1 that results in the highest payoff. This is the best response.
    """
    @staticmethod
    def best_response(payoffs, player):
        best = payoffs[0][player]
        best_index = 0

        for i in range(len(payoffs)):
            if definitely(best < payoffs[i][player]):
                best = payoffs[i][player]
                best_index = i

        return best_index

    def brute_force(self, payoff_matrix, grid_points):
        indices_p0 = []
        indices_p1 = []
        # Find the indices for the best responses for p1, given each of strategy of p0
        for row in payoff_matrix:
            indices_p1.append(self.best_response(row, 1))

        best_responses_p1 = [row[index] for row, index in zip(grid_points, indices_p1)]

        for j in range(len(payoff_matrix[0])):
            # extract the column as a list
            column = [row[j] for row in payoff_matrix]
            # find the best response for player 0 in the column
            best_response = self.best_response(column, 0)
            # append the best response index to the indices_p0 list
            indices_p0.append(best_response)

        best_responses_p0 = [row[index] for row, index in zip(grid_points, indices_p0)]
        approx_best_responses = self.nash(best_responses_p0, best_responses_p1)

        convergence = LocalConvergence()
        converged_roots = []
        for point in approx_best_responses:
            converged_roots.append(convergence.newtons(self.payoff_function, point))

        return approx_best_responses, converged_roots

    @staticmethod
    def nash(best_responses_p0, best_responses_p1):
        both_best = []

        for i in range(len(best_responses_p0)):
            for j in range(len(best_responses_p1)):
                if definitely(best_responses_p0[i] == best_responses_p1[j]):
                    both_best.append(best_responses_p0[i])

        return both_best

    @staticmethod
    def brute_force_nash_equilibrium(payoff_matrix, grid_points):
        num_rows = len(payoff_matrix)
        num_cols = len(payoff_matrix[0])

        nash_equilibria = []

        for row in range(num_rows):
            for col in range(num_cols):
                is_nash_equilibrium = True
                # Check if this combination of strategies is a Nash Equilibrium for both players
                for i in range(num_rows):
                    if definitely(payoff_matrix[row][i][0] > payoff_matrix[row][col][0]):
                        is_nash_equilibrium = False
                        break

                for j in range(num_cols):
                    if definitely(payoff_matrix[row][j][1] > payoff_matrix[row][col][1]):
                        is_nash_equilibrium = False
                        break

                if is_nash_equilibrium:
                    nash_equilibria.append(grid_points[row][col])

        return nash_equilibria
