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
    
    print("Generated interpolation points:")
    for point in points:
        print(point)
