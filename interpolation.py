import numpy as np
import sympy as sp


def get_interpolation_points(func_str, a, b, degree):
    x = sp.symbols('x')
    func = sp.sympify(func_str)
    
    # Generate n+1 points uniformly in [a, b]
    x_values = np.linspace(a, b, degree + 1)
    y_values = [func.subs(x, val).evalf() for val in x_values]
    
    return list(zip(x_values, y_values))


def read_points_from_file(filename):
    points = []
    with open(filename, 'r') as file:
        for line in file:
            x, y = map(float, line.strip().split(','))
            points.append((x, y))
    return points


# Implement the polynomial interpolation
def interpolate_sle(points):
    n = len(points)
    x = sp.symbols('x')
    A = sp.Matrix([[pt[0]**i for i in range(n)] for pt in points])
    b = sp.Matrix([pt[1] for pt in points])
    coeffs = A.LUsolve(b)
    
    # Construct the polynomial
    polynomial = sum(coeffs[i] * x**i for i in range(n))
    return polynomial.simplify()


# Implement the Lagrange polynomial interpolation
def interpolate_lagrange(points):
    x = sp.symbols('x')
    n = len(points)
    polynomial = 0
    
    for i in range(n):
        xi, yi = points[i]
        li = 1
        for j in range(n):
            if i != j:
                xj, _ = points[j]
                li *= (x - xj) / (xi - xj)
        polynomial += yi * li
    
    return polynomial.simplify()


# Implement the parametric polynomial interpolation
def interpolate_parametric(points):
    t = sp.symbols('t')
    n = len(points)
    t_values = np.linspace(0, 1, n)
    
    x_values, y_values = zip(*points)
    x_poly = interpolate_lagrange(list(zip(t_values, x_values)))
    y_poly = interpolate_lagrange(list(zip(t_values, y_values)))
    
    return x_poly, y_poly


# Implement the polynomial interpolation
if __name__ == "__main__":
    choice = input("Choose input method (1: Function, 2: File): ")
    if choice == "1":
        func_str = input("Enter a function of x (e.g., x*sin(x) - x**2 + 1): ")
        a = float(input("Enter the start of interval: "))
        b = float(input("Enter the end of interval: "))
        degree = int(input("Enter the polynomial degree: "))
        points = get_interpolation_points(func_str, a, b, degree)
    elif choice == "2":
        filename = input("Enter the filename containing points: ")
        points = read_points_from_file(filename)
    else:
        print("Invalid choice")
        exit()
    

    # Print the interpolation points
    print("Generated interpolation points:")
    for point in points:
        print(point)
    
    # Solve the system of linear equations
    polynomial_sle = interpolate_sle(points)
    print("Interpolation polynomial using SLE:", polynomial_sle)
    
    # Lagrange interpolation
    polynomial_lagrange = interpolate_lagrange(points)
    print("Interpolation polynomial using Lagrange formula:", polynomial_lagrange)

    # Parametric interpolation
    x_poly, y_poly = interpolate_parametric(points)
    print("Parametric interpolation polynomials:")
    print("x(t) =", x_poly)
    print("y(t) =", y_poly)
