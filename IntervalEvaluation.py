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
        self.ari_intervals = [[FloatDPUpperInterval(x_(lower), x_(upper), dp)]]

    """
       |This method verifies if the local maxima found are also global maxima. 
       |It evaluates intervals under 6 conditions and depending on which ones hold,
       |that will tell us whether or not the Nash is a global Nash.
       |nash: the nash equilibrium that has been found
       |intervals: the intervals in which the evaluation will be performed in
       """

    def interval_evaluation(self, nash, intervals, player):
        equilibrium = nash[player]
        interval_equilibrium = FloatDPUpperInterval(equilibrium.lower(), equilibrium.upper())
        payoff = self.payoff_function[player]
        deriv_payoff = derivative(payoff, player)
        second_deriv_payoff = derivative(deriv_payoff, player)
        results = []

        for element in intervals:
            for interval in element:
                box = FloatDPUpperBox([interval, interval_equilibrium])
                payoff_range = image(box, payoff)
                deriv_payoff_range = image(box, deriv_payoff)
                second_deriv_payoff_range = image(box, second_deriv_payoff)

                condition1 = definitely(payoff_range.upper_bound() < FloatDPLowerBound(payoff(nash), dp))
                condition2 = (definitely(deriv_payoff_range.lower_bound() > FloatDPUpperBound(0, dp)) or definitely(
                    deriv_payoff_range.upper_bound() < zero))  # no zero in the interval so f'(I) ≠ 0
                condition3 = definitely(second_deriv_payoff_range.lower_bound() > FloatDPUpperBound(0, dp))
                condition4 = definitely(payoff_range.lower_bound() > FloatDPUpperBound(payoff(nash), dp))
                condition5 = definitely(
                    second_deriv_payoff_range.upper_bound() < zero)  # and contains(interval, nash[player])

                if condition1 or condition2 or condition3:
                    # print("{} is a unique local max in {}".format(nash, interval))
                    results.append(True)

                elif condition4:
                    return False  # print("{} is not a global Nash equilibrium".format(nash))

                elif condition5:
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
        print("called split")
        return ari_intervals

    """
    |This method updates the local variables for the intervals. 
    """

    def update_intervals(self, new_intervals, ariadne):
        self.intervals = new_intervals
        self.ari_intervals = ariadne
