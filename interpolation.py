import numpy as np
import sympy as sp
import matplotlib.pyplot as plt



def get_interpolation_points(func_str, a, b, degree):
    x = sp.symbols('x')
    func = sp.sympify(func_str)
    
    # Generate n+1 points uniformly in [a, b]
    x_values = np.linspace(float(a), float(b), degree + 1)
    
    # Evaluate the function at each point
    y_values = []
    for val in x_values:
        # Use evalf() to evaluate the expression numerically
        y_val = float(func.subs(x, val).evalf())
        y_values.append(y_val)
    
    return list(zip(x_values, y_values))


# Add the following functions to the end of the file
def read_points_from_file(filename):
    points = []
    with open(filename, 'r') as file:
        for line in file:
            x, y = map(float, line.strip().split(','))
            points.append((x, y))
    return points


# Add the following functions to the end of the file
def interpolate_sle(points):
    n = len(points)
    x = sp.symbols('x')
    # Convert points to float explicitly
    A = sp.Matrix([[float(pt[0])**i for i in range(n)] for pt in points])
    b = sp.Matrix([float(pt[1]) for pt in points])
    coeffs = A.LUsolve(b)
    
    # Construct the polynomial using SymPy
    polynomial = 0
    for i in range(n):
        polynomial += coeffs[i] * x**i
    return polynomial


# Add the following functions to the end of the file
def interpolate_lagrange(points):
    x = sp.symbols('x')
    n = len(points)
    polynomial = 0
    
    for i in range(n):
        xi, yi = float(points[i][0]), float(points[i][1])
        li = 1
        for j in range(n):
            if i != j:
                xj = float(points[j][0])
                li *= (x - xj) / (xi - xj)
        polynomial += yi * li
    
    return polynomial


# Add the following functions to the end of the file
def interpolate_parametric(points):
    t = sp.symbols('t')
    n = len(points)
    t_values = list(np.linspace(0, 1, n))  # Convert to list for SymPy
    
    x_values, y_values = zip(*points)
    # Convert values to float explicitly
    x_values = [float(x) for x in x_values]
    y_values = [float(y) for y in y_values]
    x_poly = interpolate_lagrange(list(zip(t_values, x_values)))
    y_poly = interpolate_lagrange(list(zip(t_values, y_values)))
    
    return x_poly, y_poly


# Add the following functions to the end of the file
def evaluate_expression(expr, symbol, value):
    """Safely evaluate a SymPy expression at a given value."""
    try:
        result = float(expr.subs(symbol, value).evalf())
        return result
    except:
        return np.nan


# Add the following functions to the end of the file
def evaluate_polynomials_at_point(x_val, poly_sle, poly_lagrange, x_poly=None, y_poly=None):
    """Evaluate all polynomials at a given point."""
    x = sp.symbols('x')
    t = sp.symbols('t')
    
    results = {
        'SLE': evaluate_expression(poly_sle, x, x_val),
        'Lagrange': evaluate_expression(poly_lagrange, x, x_val)
    }
    
    # For parametric curves, find t value that gives closest x coordinate
    if x_poly is not None and y_poly is not None:
        t_vals = np.linspace(0, 1, 1000)
        x_coords = [evaluate_expression(x_poly, t, t_val) for t_val in t_vals]
        # Find t value where x_poly(t) is closest to x_val
        closest_t_idx = min(range(len(x_coords)), key=lambda i: abs(x_coords[i] - x_val))
        closest_t = t_vals[closest_t_idx]
        results['Parametric'] = (
            evaluate_expression(x_poly, t, closest_t),
            evaluate_expression(y_poly, t, closest_t)
        )
    
    return results

# Add the following functions to the end of the file
def plot_interpolation(points, poly_sle, poly_lagrange, x_poly, y_poly):
    x = sp.symbols('x')
    t = sp.symbols('t')
    
    # Create arrays for plotting
    x_vals = np.linspace(float(points[0][0]), float(points[-1][0]), 100)
    y_sle = [evaluate_expression(poly_sle, x, val) for val in x_vals]
    y_lagrange = [evaluate_expression(poly_lagrange, x, val) for val in x_vals]
    
    plt.figure(figsize=(10, 6))
    plt.scatter(*zip(*points), color='red', label='Interpolation Points')
    plt.plot(x_vals, y_sle, label='SLE Polynomial', linestyle='dashed')
    plt.plot(x_vals, y_lagrange, label='Lagrange Polynomial', linestyle='dotted')
    
    if x_poly is not None and y_poly is not None:
        t_vals = np.linspace(0, 1, 100)
        x_param = [evaluate_expression(x_poly, t, val) for val in t_vals]
        y_param = [evaluate_expression(y_poly, t, val) for val in t_vals]
        plt.plot(x_param, y_param, label='Parametric Interpolation', linestyle='dashdot')
    
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Interpolation Polynomials')
    plt.grid()
    plt.show()


# Add the following code to the end of the file
if __name__ == "__main__":
    choice = input("Choose input method (1: Function, 2: File): ")
    
    try:
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
        

        # Perform interpolation
        print("\nGenerated interpolation points:")
        for point in points:
            print(f"({point[0]:.4f}, {point[1]:.4f})")
        
        # Interpolation using SLE
        polynomial_sle = interpolate_sle(points)
        print("\nInterpolation polynomial using SLE:", polynomial_sle)
        
        # Interpolation using Lagrange
        polynomial_lagrange = interpolate_lagrange(points)
        print("\nInterpolation polynomial using Lagrange formula:", polynomial_lagrange)

        # Interpolation using parametric curves   
        x_poly, y_poly = interpolate_parametric(points)
        print("\nParametric interpolation polynomials:")
        print("x(t) =", x_poly)
        print("y(t) =", y_poly)

        plot_interpolation(points, polynomial_sle, polynomial_lagrange, x_poly, y_poly)
        
        # Add point evaluation functionality
        while True:
            try:
                eval_choice = input("\nWould you like to evaluate the polynomials at a specific point? (y/n): ")
                if eval_choice.lower() != 'y':
                    break
                    
                x_val = float(input("Enter x value: "))
                if x_val < min(p[0] for p in points) or x_val > max(p[0] for p in points):
                    print("Warning: Point is outside the interpolation interval!")
                    
                results = evaluate_polynomials_at_point(x_val, polynomial_sle, polynomial_lagrange, x_poly, y_poly)
                
                
                print(f"\nValues at x = {x_val}:")
                print(f"SLE Polynomial: {results['SLE']:.6f}")
                print(f"Lagrange Polynomial: {results['Lagrange']:.6f}")
                if 'Parametric' in results:
                    param_x, param_y = results['Parametric']
                    print(f"Parametric Interpolation: ({param_x:.6f}, {param_y:.6f})")
                    
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e