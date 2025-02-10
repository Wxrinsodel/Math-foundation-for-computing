from flask import Flask, render_template, request
import sympy as sp
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

app = Flask(__name__)

def bisection_method(f, a, b, tol):
    iterations = 0
    errors = []
    
    if f(a) * f(b) > 0:
        return None, None, None  # Root may not exist in the interval
    
    while (b - a) / 2.0 > tol:
        iterations += 1
        midpoint = (a + b) / 2.0
        errors.append(abs(f(midpoint)))
        
        if f(midpoint) == 0 or (b - a) / 2.0 < tol:
            return midpoint, iterations, errors
        
        if f(a) * f(midpoint) < 0:
            b = midpoint
        else:
            a = midpoint

    return (a + b) / 2.0, iterations, errors

def newton_method(f, f_prime, x0, tol):
    iterations = 0
    errors = []
    x = x0
    
    while True:
        iterations += 1
        if f_prime(x) == 0:
            return None, None, None  # Avoid division by zero
        
        x_new = x - f(x) / f_prime(x)
        errors.append(abs(f(x_new)))
        
        if abs(x_new - x) < tol:
            return x_new, iterations, errors
        
        x = x_new

@app.route('/', methods=['GET', 'POST'])
def index():
    root_bisection, iterations_bisection, errors_bisection = None, None, None
    root_newton, iterations_newton, errors_newton = None, None, None
    plot_url = None

    if request.method == 'POST':
        function_str = request.form['function']
        try:
            a = float(request.form['a'])
            b = float(request.form['b'])
            tol = float(request.form['tol'])
        except ValueError:
            return "Invalid numeric input"

        x = sp.symbols('x')
        try:
            expr = sp.sympify(function_str)
            f = sp.lambdify(x, expr, 'numpy')
            f_prime = sp.lambdify(x, sp.diff(expr, x), 'numpy')
        except Exception as e:
            return f"Error parsing function: {e}"

        try:
            root_bisection, iterations_bisection, errors_bisection = bisection_method(f, a, b, tol)
            root_newton, iterations_newton, errors_newton = newton_method(f, f_prime, (a + b) / 2.0, tol)
        except Exception as e:
            return f"Error solving root-finding problem: {e}"

        if root_bisection is not None and root_newton is not None:
            plt.figure()
            plt.plot(range(1, iterations_bisection + 1), errors_bisection, label='Bisection')
            plt.plot(range(1, iterations_newton + 1), errors_newton, label='Newton')
            plt.xlabel('Iterations')
            plt.ylabel('Error')
            plt.title('Convergence Graph')
            plt.legend()
            
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            plt.close()

        return render_template('index.html', root_bisection=root_bisection, iterations_bisection=iterations_bisection,
                               root_newton=root_newton, iterations_newton=iterations_newton, plot_url=plot_url)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=21002 , debug=True)
