from pyariadne import *

x = RealVariable("x")
y = RealVariable("y")
f = make_function([x, y], [-x**2 + 2*x*y - y**2, -x**3 - y**4 + 3*x*y])  # root at (5,3)
print('f(x, y)=', f)

# to evaluate the interval
exact_interval = FloatDPExactInterval(x_(-1.25), x_(1))
upper_interval = FloatDPUpperInterval(x_(-1.25), x_(1), dp)
print(exact_interval)
print(upper_interval)

#print(f(exact_interval))  # doesn't work
#print(evaluate(f, interval))  # also doesn't work

print(midpoint(exact_interval))
