import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Define the function
def f(x, y):
    return -x**2 + 2*x*y - y**2  # -x ** 3 - y ** 3 + 3 * x * y


# Create grid points for x and y
x = np.linspace(-2, 2, 100)
y = np.linspace(-2, 2, 100)
X, Y = np.meshgrid(x, y)

# Compute the corresponding function values
Z = f(X, Y)

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
ax.plot_surface(X, Y, Z, cmap='viridis')

# Highlight critical points
critical_points = [(0, 0), (1, 1)]
for point in critical_points:
    x, y = point
    z = f(x, y)
    ax.scatter(x, y, z, color='red', s=50)

# Set labels and title
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('f(x, y)')
ax.set_title('Plot of f(x, y) = -x^3 - y^3 + 3xy')

# Show the plot
plt.show()
