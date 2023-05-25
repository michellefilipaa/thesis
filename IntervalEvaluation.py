from pyariadne import *
from DifferentialGame import DifferentialGame

x = RealVariable("x")
y = RealVariable("y")
check_max = DifferentialGame()
zero = FloatDPBounds(0, dp)


class IntervalEvaluation:

    def __init__(self, payoff_function, lower=-1.25, upper=1):
        self.payoff_function = payoff_function
        self.lower = lower
        self.upper = upper
        self.interval = [FloatDPUpperInterval(x_(lower), x_(upper), dp)]

    def interval_evaluation(self, nash, intervals):
        for interval in intervals:
            condition1 = definitely(self.payoff_function(interval) < self.payoff_function(nash))
            condition2 = not definitely(derivative(interval) == zero)
            condition3 = definitely(derivative(interval) > zero)
            condition4 = definitely(self.payoff_function(interval) > self.payoff_function(nash))
            condition5 = not condition4
            condition6 = definitely(check_max.test_local_max(self.payoff_function, interval) < zero)

            if condition1 or condition2 or condition3:
                print("{} is a unique local max in {}".format(nash, interval))

            elif condition4:
                print("{} is not a global Nash equilibrium".format(nash))

            elif condition5 and condition6:
                print("{} is a unique local max in {}".format(nash, interval))

            else:
                return self.interval_evaluation(nash, self.split_intervals(interval))

    @staticmethod
    def split_intervals(intervals):
        # TODO: ariadne-fy this
        new_intervals = []
        for interval in intervals:
            start, end = interval
            mid_point = midpoint(interval)
            new_intervals.append([start, mid_point])
            new_intervals.append([mid_point, end])

        return new_intervals

    """
    |This method verifies if the local maxima found are also global maxima.
    |payoffs: the payoffs given by the strategy function of each player
    |nash_strategies: the strategy combinations that have been found to be nash equilibria
    |all_x: the other strategy points that will be evaluated against the nash strategy
    |player: 0 or 1, depending on which player is being evaluated
    """
    @staticmethod
    def interval_evaluation2(payoffs, nash_strategy, all_x, player):
        payoff = payoffs[player]
        y_star = nash_strategy[player - 1]
        max_check = []

        for x in all_x:
            if definitely(nash_strategy[0] == x):
                continue
            else:
                new_strat = FloatDPBoundsVector([x, y_star], dp)
                if definitely(payoff(nash_strategy) > payoff(new_strat)):
                    continue
                else:
                    max_check.append(False)
                    print("{} {} leads to higher payoff".format('Not Global Maximum', x))

        return print("Global max" if all(max_check) else "{} Not Global Max".format(nash_strategy))


