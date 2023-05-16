import matplotlib.pyplot as plt
import numpy as np


def plot_functions(self):
    x = np.arange(-5, 5, 0.1)
    y = np.arange(-5, 5, 0.1)
    xx, yy = np.meshgrid(x, y)

    zz = self.player_1(xx)
    plt.contour(xx, yy, zz)
    plt.xlabel('x')
    plt.ylabel('y')

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(xx, yy, zz)

    plt.show()


@staticmethod
def player_1(x):
    return 2 * x - 1


@staticmethod
def player_2(y):
    return 3 * y - 1