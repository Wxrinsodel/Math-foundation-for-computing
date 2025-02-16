import numpy as np
import sympy as sp



def get_interpolation_points(func_str, a, b, degree):
    x = sp.symbols('x')
    func = sp.sympify(func_str)
    
    # Generate n+1 points uniformly in [a, b]
    x_values = np.linspace(a, b, degree + 1)
    y_values = [func.subs(x, val).evalf() for val in x_values]
    
    return list(zip(x_values, y_values))


# Read points from a file
def read_points_from_file(filename):
    points = []
    with open(filename, 'r') as file:
        for line in file:
            x, y = map(float, line.strip().split(','))
            points.append((x, y))
    return points


# Interpolate using a system of linear equations
def interpolate_sle(points):
    n = len(points)
    x = sp.symbols('x')
    A = sp.Matrix([[pt[0]**i for i in range(n)] for pt in points])
    b = sp.Matrix([pt[1] for pt in points])
    coeffs = A.LUsolve(b)
    
    polynomial = sum(coeffs[i] * x**i for i in range(n))
    return polynomial.simplify()


# Interpolate using Lagrange polynomials
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
    
    polynomial = interpolate_sle(points)
    print("Interpolation polynomial using SLE:", polynomial) 
