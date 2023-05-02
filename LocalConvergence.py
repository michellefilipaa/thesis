from pyariadne import *

x = RealVariable("x")
y = RealVariable("y")


class LocalConvergence:
    @staticmethod
    def newtons_1d(payoffs, x_n):
        f_x_n = payoffs(x_n)
        f_deriv = derivative(payoffs, 0)
        return x_n - (f_x_n/f_deriv(x_n))

    @staticmethod
    def newtons_2d_plus(payoffs, x_n):
        j = jacobian(payoffs, x_n)
