from pyariadne import *

x = RealVariable("x")
y = RealVariable("y")


class DifferentialGame:
    def __init__(self, tolerance=1e-6, max_steps=32):
        self.tolerance = tolerance
        self.max_steps = max_steps

    """
    |This method finds the roots for the player.
    |solver: either the Interval Newton or Krawczyk solver
    |payoffs: the payoffs for each player
    |p0_deriv: the derivative of the payoff with respect to player 1
    |p1_deriv: the derivative of the payoff with respect to player 2
    |Returns -> the roots found which are potential Nash equilibria
    """
    @staticmethod
    def find_roots(solver, payoffs, lower_bound=-1.25, upper_bound=1):
        p0_deriv = derivative(payoffs[0], 0)
        p1_deriv = derivative(payoffs[1], 1)
        g = join(p0_deriv, p1_deriv)

        interval = IntervalDomainType([pr_(lower_bound), pr_(upper_bound)])
        region = BoxDomainType([interval, interval])

        roots = solver.solve_all(g, region)

        return roots

    """
    |This method checks if the second derivative is less than 0 at the point where the first derivative is 0.
    |If so, then it is a local maximum. If not, then it is either an arbitrary stationary point or a local minimum.
    |Return: True if both points are local maxima, False if not.
    """
    @staticmethod
    def test_local_max(payoffs, roots):
        check_roots = []
        for root in roots:
            p0_2nd_deriv = derivative(derivative(payoffs[0], 0), 0)
            p1_2nd_deriv = derivative(derivative(payoffs[1], 1), 1)

            value_p0 = evaluate(p0_2nd_deriv, root)
            value_p1 = evaluate(p1_2nd_deriv, root)

            zero = FloatDPBounds(0, dp)

            check_roots.append(definitely((value_p0 < zero) & (value_p1 < zero)))

        return check_roots

    @staticmethod
    def payoff_at_max(payoffs, check_roots, roots):
        payoff_values = []
        for i in range(len(check_roots)):
            if check_roots[i] is True:
                payoff_values.append(payoffs(roots[i]))

        return payoff_values
