import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange

def build_vandermonde_matrix(x_values):
    """Build the Vandermonde matrix for interpolation."""
    m = len(x_values)  # Number of interpolation points
    V = np.vander(x_values, increasing=True)
    return V

def interpolate_function(f, a, b, m):
    """Construct an interpolation polynomial using a system of linear equations."""
    x_values = np.linspace(a, b, m)
    y_values = f(x_values)
    
    V = build_vandermonde_matrix(x_values)  # Vandermonde matrix
    coefficients, _, _, _ = np.linalg.lstsq(V, y_values, rcond=None)  # Using least squares
    
    return coefficients, x_values, y_values

# Implement the polynomial interpolation

def polynomial(coefficients, x):
    """Evaluate the interpolation polynomial at x."""
    return np.polyval(coefficients[::-1], x)

def plot_interpolation(f, a, b, coefficients, x_values, y_values):
    """Plot the original function and the interpolation polynomials."""
    x_plot = np.linspace(a, b, 1000)
    y_plot = f(x_plot)
    y_interp = np.polyval(coefficients[::-1], x_plot)
    
    lagrange_poly = lagrange(x_values, y_values)
    y_lagrange = lagrange_poly(x_plot)
    
    plt.plot(x_plot, y_plot, label="Original function", linestyle="dashed")
    plt.plot(x_plot, y_interp, label="Interpolation polynomial (SLE)", linewidth=2)
    plt.plot(x_plot, y_lagrange, label="Interpolation polynomial (Lagrange)", linewidth=2, linestyle="dotted")
    plt.scatter(x_values, y_values, color="red", label="Interpolation points")
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Interpolation using SLE and Lagrange")
    plt.show()

if __name__ == "__main__":
    # Experiment with different functions and number of points
    functions = [
        lambda x: np.sin(8 * x),
        lambda x: np.sin(5 * x),
        lambda x: np.exp(x),
        lambda x: x**2 + 2*x + 1
    ]
    
    intervals = [
        (0, np.pi),
        (0, 2 * np.pi),
        (0, 1),
        (-1, 1)
    ]
    
    points = [4, 5, 7, 8, 10]
    
    for f, (a, b), m in zip(functions, intervals, points):
        coefficients, x_values, y_values = interpolate_function(f, a, b, m)
        plot_interpolation(f, a, b, coefficients, x_values, y_values)