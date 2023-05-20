from pyariadne import *
import random

x = RealVariable("x")
y = RealVariable("y")
f = make_function([x, y], [-x ** 2 - y ** 2 + 10 * x + 6 * y])  # root at (5,3)
print('f(x, y)=', f)
'''
gives the derivative of f, in terms of x
'''
f_deriv = derivative(f, 0)

'''
input make_function([x], [x**2 + x**3])
output -> [pow(x0,2)+pow(x0,3)]
this means x0^2 + x0^3

input make_function([x,y], [x**2 + x**3 + y])
output -> [pow(x0,2)+pow(x0,3)+x1]
this means x0^2 + x0^3 + x1
where x0 = x and x1 = y
'''
# find roots
tolerance = 1e-6
max_steps = 32

# ! The IntervalNewtonSolver is rather more sensitive
# ! but we can still compute the inverse given sufficiently tight bounds
lower_bound = 0.0
upper_bound = 6.0

g = make_function([x, y],
                  [2 * x - 1, 3 * y - 1])  # why is there a comma in the middle of the function? What does that mean
# PC: You need "region" to have one interval component for each player's strategy.
# interval = IntervalDomainType([pr_(lower_bound), pr_(upper_bound)])  # PC
interval = IntervalDomainType([0, 6])  # PC
region = BoxDomainType([interval, interval])  # PC
solver = IntervalNewtonSolver(tolerance, max_steps)
print("g:", g)
print("region:", region)
p = solver.solve(g, region)
print('Roots=', type(p))

"""
PC: Use of 'p' here is confusing, since p1, p2 are different kinds of object
PC: The method should return the root(s)!
PC: The solver returns a list or set of roots, so you need to iterate to print
"""
# for root in p:
# print("g(", root, "):", g(root))  # value of function at root

# how do I evaluate the function f(x) at x = 2 and y = 1?
v = Vector[FloatDPBounds]([2, 1], dp)
print('Value of f(2,1) =', evaluate(f, v))
print("Derivative at (2,1) =", evaluate(g, v))

print(FloatDPBounds(2, dp))

"""
region = BoxDomainType([[pr_(0.1), pr_(1)]])

solver = KrawczykSolver(tolerance, max_steps)
p = solver.solve(g, region)
print("p=fix(f):", p)
print("f(p):", g(p))
print("\n")
"""


