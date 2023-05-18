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
        compare_p0 = [payoff[0] for payoff in payoffs]
        compare_p1 = [payoff[1] for payoff in payoffs]

        self.compare_payoffs(compare_p0, nash_strategies, "p0")
        self.compare_payoffs(compare_p1, nash_strategies, "p1")


    """
    |This method compares the payoff of each nash equilbria to determine which strategy is best 
    |for each player.
    |It creates pairs of all elements in the list for comparison.
    |It then prints which strategy leads to the highest payoff. 
    """
    @staticmethod
    def compare_payoffs(payoffs, strategies, player):
        max_payoff = None
        for s1, s2 in zip(payoffs[:-1], payoffs[1:]):
            if possibly(s1 > s2):
                max_payoff = s1

            elif possibly(s1 < s2):
                max_payoff = s2

        # TODO: change from returning payoff to returning strategy

        if max_payoff is not None:
            print(max_payoff, "is best for", player)
            return max_payoff

    """
    |This method verifies if the local maxima found are also global maxima.
    |payoffs: the payoffs given by the strategy function of each player
    |nash_strategies: the strategy combinations that have been found to be nash equilibria
    |all_x: the other strategy points that will be evaluated against the nash strategy
    |player: 0 or 1, depending on which player is being evaluated
    """
    @staticmethod
    def interval_evaluation(payoffs, nash_strategy, all_x, player):
        payoff = payoffs[player]
        y_star = nash_strategy[player-1]

        for x in all_x:
            new_strat = FloatDPBoundsVector([x, y_star], dp)
            if definitely(payoff(nash_strategy) > payoff(new_strat)):
                continue
            else:
                return "{} {} leads to higher payoff".format('Not Global Maximum', x)

        return "Global Max"

