import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def f(x):
    return (x**2) - 5 

a, b, tol = -3, 2, 1e-10


def bisection_with_tracking(a, b, tol):
    approximations = []
    
    for _ in range(100):
        m = (a + b) / 2
        approximations.append(m)

        if abs(f(m)) < tol or (b - a) / 2 < tol:
            break

        if f(a) * f(m) < 0:
            b = m
        else:
            a = m

    return approximations

approximations = bisection_with_tracking(a, b, tol)

x = np.linspace(a, b, 400)
y = f(x)

fig, ax = plt.subplots()
ax.plot(x, y, label="f(x)")
ax.axhline(0, color="black", linewidth=0.1)
approx_dots, = ax.plot([], [], "ro", markersize=5, label="Approximations")

def update(i):
    approx_dots.set_data(approximations[:i+1], [0] * (i+1))
    return approx_dots,

ani = animation.FuncAnimation(fig, update, frames=len(approximations), interval=500, repeat=False)

plt.legend()
plt.show()
