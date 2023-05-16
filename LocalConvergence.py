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
    def nash_evaluation(payoffs, roots):
        # payoffs[i][j] is the payoff player j at root i.
        if possibly(payoffs[0][0] > payoffs[1][0]):
            print("yes")
            if definitely(payoffs[0][1] > payoffs[1][1]):
                print("yes2")
                return roots[0]

            else:
                print("no2")
        else:
            print("no")
