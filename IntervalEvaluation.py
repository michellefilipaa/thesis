from pyariadne import *
from DifferentialGame import DifferentialGame

x = RealVariable("x")
y = RealVariable("y")
check_max = DifferentialGame()
zero = FloatDPLowerBound(0, dp)


class IntervalEvaluation:

    def __init__(self, payoff_function, lower=-1.25, upper=1):
        self.payoff_function = payoff_function
        self.lower = lower
        self.upper = upper
        self.intervals = [[lower, upper]]
        self.ari_intervals = [[FloatDPUpperInterval(x_(upper), x_(lower), dp)]]

    """
       |This method verifies if the local maxima found are also global maxima. 
       |It evaluates intervals under 6 conditions and depending on which ones hold,
       |that will tell us whether or not the Nash is a global Nash.
       |nash: the nash equilibrium that has been found
       |intervals: the intervals in which the evaluation will be performed in
       """
    def interval_evaluation(self, nash, intervals, player):
        interval_equilibrium = FloatDPUpperInterval(nash[player].lower(), nash[player].upper())
        f = self.payoff_function[player]
        results = []

        for element in intervals:
            for interval in element:
                box = FloatDPUpperBox([interval, interval_equilibrium])
                payoff_range = image(box, f)
                deriv_payoff_range = image(box, derivative(f, player))
                second_deriv_payoff_range = image(box, derivative(derivative(f, player), player))

                condition1 = definitely(payoff_range.upper_bound() < FloatDPLowerBound(f(nash), dp))
                condition2 = (definitely(deriv_payoff_range.lower_bound() < FloatDPUpperBound(0, dp)) or definitely(
                    deriv_payoff_range.upper_bound() > zero))
                condition3 = definitely(second_deriv_payoff_range.upper_bound() > zero)
                condition4 = definitely(payoff_range.lower_bound() > FloatDPUpperBound(f(nash), dp))
                condition5 = not condition4
                condition6 = not condition3

                if condition1 or condition2 or condition3:
                    # print("{} is a unique local max in {}".format(nash, interval))
                    results.append(True)

                elif condition4:
                    # print("{} is not a global Nash equilibrium".format(nash))
                    results.append(False)

                elif condition5 and condition6:
                    # print("{} is a unique local max in {}".format(nash, interval))
                    results.append(True)

        if not results:
            results.extend(self.interval_evaluation(nash, self.split_intervals(self.intervals), player))

        return results

    """
    |This method splits an interval into two.
    |Returns: a list of Ariadne object intervals
    """
    def split_intervals(self, intervals):
        new_intervals = []
        for interval in intervals:
            start, end = interval
            mid_point = (start + end) / 2
            new_intervals.append([start, mid_point])
            new_intervals.append([mid_point, end])

        ari_intervals = [[FloatDPUpperInterval(x_(interval[0]), x_(interval[1]), dp)] for interval in new_intervals]
        self.update_intervals(new_intervals, ari_intervals)

        return ari_intervals

    """
    |This method updates the local variables for the intervals. 
    """
    def update_intervals(self, new_intervals, ariadne):
        self.intervals = new_intervals
        self.ari_intervals = ariadne
