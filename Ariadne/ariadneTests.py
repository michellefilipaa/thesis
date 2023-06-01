from pyariadne import *

x = RealVariable("x")
y = RealVariable("y")
f = make_function([x, y], [-x**2 + 2*x*y - y**2, -x**3 - y**4 + 3*x*y])  # root at (5,3)
print('f(x, y)=', f)

v = Vector[FloatDPBounds]([2, 1], dp)

# to evaluate the interval
exact_interval = FloatDPExactInterval(x_(-1.25), x_(1))
upper_interval = FloatDPUpperInterval(x_(-1.25), x_(1), dp)
# print(evaluate(f, exact_interval))
# print(f(Vector[upper_interval]))

# PC
print("\nSetting-up test interval evaluation\n")
payoff0 = f[0]
deriv_payoff0 = derivative(payoff0,0)
equilibrium1 = FloatDPBounds(x_(0.5), dp)
interval0 = FloatDPUpperInterval(x_(0.0), x_(0.5), dp)
print(payoff0, equilibrium1, interval0)

# Conpute ranges as Bounds values
#singleton0=cast_singleton(interval0)
#box_vector=FloatDPBoundsVector([singleton0,equilibrium1])
#print("f0(ivl0,nash1)",payoff0(box_vector))
#print("df0(ivl0,nash1)", deriv_payoff0(box_vector))

# Compute ranges as Intervals
interval_equilibrium1 = FloatDPUpperInterval(equilibrium1.lower(), equilibrium1.upper())
box = FloatDPUpperBox([interval0, interval_equilibrium1])
payoff0_range = image(box, payoff0)
deriv_payoff0_range = image(box, deriv_payoff0)

print(payoff0_range.lower_bound() > FloatDPUpperBound(0, dp))
print(definitely(payoff0_range.lower_bound() > FloatDPUpperBound(0, dp)))
print(payoff0_range.upper_bound() >= FloatDPLowerBound(0, dp))
print(possibly(payoff0_range.upper_bound() > FloatDPLowerBound(0, dp)))

print("payoff0_range", payoff0_range)
print("deriv_payoff0_range", deriv_payoff0_range)



