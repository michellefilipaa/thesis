from pyariadne import *

x = RealVariable("x")
y = RealVariable("y")


class LocalConvergence:
    @staticmethod
    def newtons(payoffs, xy):
        p0_deriv = derivative(payoffs[0], 0)
        p1_deriv = derivative(payoffs[1], 1)
        g = join(p0_deriv, p1_deriv)

        previous_xy = xy
        new_xy = xy - solve(jacobian(g, xy), g(xy))

        while definitely(new_xy != previous_xy):
            previous_xy = new_xy
            new_xy = new_xy - solve(jacobian(g, new_xy), g(new_xy))

        return new_xy

    """
    |This method compares the payoff of each nash equilbria to determine which strategy is best 
    |for each player.
    |payoffs: the payoff for each given strategy that is a nash equilibrium
    |nash_strategies: the strategy combinations which are nash equilibria
    """
    def nash_evaluation(self, payoffs, nash_strategies):
        self.compare_payoffs(payoffs[0], nash_strategies, "p0")
        self.compare_payoffs(payoffs[1], nash_strategies, "p1")


    """
    |This method compares the payoff of each nash equilbria to determine which strategy is best 
    |for each player.
    |It creates pairs of all elements in the list for comparison.
    |It then prints which strategy leads to the highest payoff. 
    """
    @staticmethod
    def compare_payoffs(payoff_function, strategies, player):
        max_strategy = None
        max_payoff = FloatDPBounds(-100000, dp)

        for s in strategies:
            payoff = evaluate(payoff_function, s)[player]
            if definitely(payoff > max_payoff):
                max_strategy = s
                max_payoff = payoff

        if max_strategy is not None:
            print(max_strategy, "is best for player", player)
            return max_strategy

