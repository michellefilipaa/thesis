import numpy as np
import sympy as sp
import random


class MatrixGame:
    def __init__(self):
        self.p1 = self.function_to_matrix()
        self.p2 = self.function_to_matrix()
        self.n = 3
        self.m = 3

        payoffs = self.get_payoffs(self.p1, self.p2)
        print('Expected Payoffs are ', payoffs)

        nash = self.best_response(payoffs, self.actions(1), self.actions(2))
        print(nash)

    """ 
    Generates a random function for the players
    """

    def strategy(self, x):
        if x is None:
            x = sp.Symbol('x')

        a = random.randint(-100, 100)
        b = random.randint(-100, 100)
        c = random.randint(-100, 100)

        return a * x ** 2 + b * x + c
    """"
        This method converts the function for the player to the payoff matrix.
    """
    def function_to_matrix(self):
        payoffs = np.zeros((self.n, self.m))

        for i in range(self.n):
            for j in range(self.m):
                payoffs[i, j] = self.strategy(i / (self.n - 1))

        print(payoffs)
        return payoffs

    def actions(self, player_no):
        if player_no == 1:
            start_char = ord('A')
            actions = [chr(start_char + i) for i in range(self.n)]
        else:
            start_char = ord('Z')
            actions = [chr(start_char - i) for i in range(self.m)]
        return actions

    def get_payoffs(self, p1_actions, p2_actions):
        expected_payoffs = np.empty((len(p1_actions), len(p2_actions), 2))

        for i in range(len(p1_actions)):
            for j in range(len(p2_actions)):
                p1_payoff = self.p1[i][j]
                p2_payoff = self.p2[j][i]
                expected_payoffs[i][j] = (p1_payoff, p2_payoff)

        return expected_payoffs

    def best_response(self, expected_payoffs, p1_actions, p2_actions):
        # Find the best response strategy for each player
        p1_best_response = np.argmax(expected_payoffs[:, :, 1], axis=0)
        p2_best_response = np.argmax(expected_payoffs[:, :, 0], axis=0)

        nash = None

        for i in range(len(p1_actions)):
            for j in range(len(p2_actions)):
                if p1_best_response[j] == i and p2_best_response[i] == j:
                    nash = (p1_actions[i], p2_actions[j])
                    print("Nash equilibrium found: Player 1 chooses", p1_actions[i], "and Player 2 chooses",
                          p2_actions[j])
        return nash


game = MatrixGame()
