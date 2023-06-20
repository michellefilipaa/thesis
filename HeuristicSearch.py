from pyariadne import *
import numpy as np
from LocalConvergence import LocalConvergence


class HeuristicSearch:
    def __init__(self, payoff_function, lower_bound=-1, upper_bound=1):
        self.payoff_function = payoff_function
        # PC: Suggest using a Box with lower and upper bounds for each player
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    """
    |This method creates a grid of strategies for each player at intervals of 'spacing'.
    |These will be used to find potential approximate Nash equilibria.
    |Returns: a grid of possible strategies
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

    """
    |This method finds the best response for each player given a set of strategies within certain bounds.
    |payoff_matrix: the matrix of the payoff values of each set of strategies
    |grid_points: an approximate set of all possible strategies within certain bounds
    |Returns: the approximate best responses and the exact values of the best response.
    """
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
        result = "No common best response found" if len(approx_best_responses) == 0 else approx_best_responses

        roots = self.converged_roots(approx_best_responses)
        roots_result = "Unable to find exact roots without best responses" if len(roots) == 0 else roots
        return result, roots_result

    """
    |This method checks which best response strategies for p0 and p1 are common.
    |These mutual best responses are Nash Equilibria.
    |best_responses_p0: the best response strategies found for p0
    |best_responses_p1: the best response strategies found for p1
    """
    @staticmethod
    def nash(best_responses_p0, best_responses_p1):
        mutual_best = []

        for i in range(len(best_responses_p0)):
            for j in range(len(best_responses_p1)):
                if definitely(best_responses_p0[i] == best_responses_p1[j]):
                    mutual_best.append(best_responses_p0[i])

        return mutual_best

    """
    |This method finds the highest payoff in each row and checks if it is the highest for each player.
    |If it is, then it is marked as a Nash Equilibrium.
    |Returns: the approximate strategies
    """
    def brute_force_nash_equilibrium(self, payoff_matrix, grid_points):
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

        return nash_equilibria, self.converged_roots(nash_equilibria)

    def converged_roots(self, approx_best_responses):
        convergence = LocalConvergence()
        converged_roots = []
        for point in approx_best_responses:
            converged_roots.append(convergence.newtons(self.payoff_function, point))

        return converged_roots
