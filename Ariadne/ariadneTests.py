from pyariadne import *

from DifferentialGame import DifferentialGame

x = RealVariable("x")
y = RealVariable("y")
f = make_function([x, y], [-x**2 + 2*x*y - y**2, -x**3 - y**4 + 3*x*y])
print('f(x, y)=', f)

game = DifferentialGame()
roots = game.find_roots(IntervalNewtonSolver(game.tolerance, game.max_steps), f)

# PC
print("\nSetting-up test interval evaluation\n")
f = make_function([x, y], [-x**2 + 2*x*y - y**2, -x**3 - y**4 + 3*x*y])
payoff0 = f[0]
deriv_payoff0 = derivative(payoff0, 0)
equilibrium = roots[0][0]
intervals = [[FloatDPUpperInterval(x_(-1.25), x_(1), dp)]]

interval_equilibrium = FloatDPUpperInterval(equilibrium.lower(), equilibrium.upper())
for element in intervals:
    for interval in element:
        box = FloatDPUpperBox([interval, interval_equilibrium])
        payoff0_range = image(box, payoff0)
        deriv_payoff0_range = image(box, deriv_payoff0)

        print("payoff0_range", payoff0_range)
        print("deriv_payoff0_range", deriv_payoff0_range)


# print(payoff0_range.lower_bound() > FloatDPUpperBound(0, dp))
# print(definitely(payoff0_range.lower_bound() > FloatDPUpperBound(0, dp)))
# print(payoff0_range.upper_bound() >= FloatDPLowerBound(0, dp))
# print(possibly(payoff0_range.upper_bound() > FloatDPLowerBound(0, dp)))


#print("contains 1:", contains(interval0, FloatDP(1, dp)))
#print("contains 0.3:", contains(interval0, FloatDP(x_(0.3), dp)))
#print("done")

# Compute ranges as Bounds values
# singleton0=cast_singleton(interval0)
# box_vector=FloatDPBoundsVector([singleton0,equilibrium1])
# print("f0(ivl0,nash1)",payoff0(box_vector))
# print("df0(ivl0,nash1)", deriv_payoff0(box_vector))
