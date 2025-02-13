import numpy as np
import matplotlib.pyplot as plt


def build_vandermonde_matrix(x_values):
    """Build the Vandermonde matrix for interpolation."""
    m = len(x_values)  # Number of interpolation points
    V = np.vander(x_values, increasing=True)
    return V

def interpolate_function(f, a, b, m):
    """Construct an interpolation polynomial using a system of linear equations."""
    x_values = np.linspace(a, b, m)
    y_values = f(x_values)
    
    V = build_vandermonde_matrix(x_values) # Vandermonde matrix
    coefficients = np.linalg.solve(V, y_values)
    
    return coefficients, x_values, y_values

def polynomial(coefficients, x):
    """Evaluate the interpolation polynomial at x."""
    return sum(c * x**i for i, c in enumerate(coefficients))


# Lagrange interpolation
def lagrange_polynomial(x_values, y_values, x):
    """Evaluate the Lagrange interpolation polynomial at x."""
    def L(k, x):
        """Compute the k-th Lagrange basis polynomial at x."""
        terms = [(x - x_values[j]) / (x_values[k] - x_values[j]) for j in range(len(x_values)) if j != k]
        return np.prod(terms) # Product of terms
    
    return sum(y_values[k] * L(k, x) for k in range(len(x_values)))


# Plotting functions
def plot_interpolation(f, a, b, coefficients, x_values, y_values):
    """Plot the original function and the interpolation polynomials."""
    x_plot = np.linspace(a, b, 1000)
    y_plot = f(x_plot)
    y_interp = [polynomial(coefficients, x) for x in x_plot]
    y_lagrange = [lagrange_polynomial(x_values, y_values, x) for x in x_plot]
    
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
    f = lambda x: np.sin(3*(x)) 
    a, b, m = 0, np.pi, 5
    
    coefficients, x_values, y_values = interpolate_function(f, a, b, m)
    plot_interpolation(f, a, b, coefficients, x_values, y_values)
