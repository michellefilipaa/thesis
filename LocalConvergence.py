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

    @staticmethod
    def nash_evaluation(payoffs, nash_strategies):
        # payoffs[i][j] is the payoff player j at root i.

        for i in range(len(nash_strategies)):
            for j in range(len(nash_strategies)):
                if possibly(payoffs[i][0] > payoffs[j][0]):
                    print("1", nash_strategies[i], "(", i, ")", "better for p0")
                else:
                    print("2", nash_strategies[j], "(", j, ")", " better for p0")

                if possibly(payoffs[i][1] > payoffs[j][1]):
                    print("3", nash_strategies[i], "(", i, ")", " better for p1")
                else:
                    print("4", nash_strategies[j], "(", j, ")", " better for p1")

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
            x_strat = x[player]
            print(x_strat)
            if definitely(payoff(nash_strategy) > payoff([x_strat, y_star])):
                continue
            else:
                print("Not Global Maximum", x_strat, "leads to higher payoff")

        print("Global Max")
