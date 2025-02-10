from flask import Flask, render_template, request
import sympy as sp
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

app = Flask(__name__) 


# Define the bisection method
def bisection_method(f, a, b, tol): 
    iterations = 0
    errors = [] # Store the error at each iteration
    
    if f(a) * f(b) > 0:
        return None, None, None  # Root may not exist in the interval
    
    while (b - a) / 2.0 > tol:
        iterations += 1
        m = (a + b) / 2.0 
        errors.append(abs(f(m))) # Calculate the error at the m
        
        if f(m) == 0 or (b - a) / 2.0 < tol:
            return m, iterations, errors
        
        if f(a) * f(m) < 0:
            b = m
        else:
            a = m

    return (a + b) / 2.0, iterations, errors


# Define the Newton method
def newton_method(f, f_prime, x0, tol): 
    iterations = 0
    errors = []
    x = x0
    
    while True:
        iterations += 1
        if f_prime(x) == 0:
            return None, None, None  # Avoid division by zero
        
        x_new = x - f(x) / f_prime(x) # Compute the next x
        errors.append(abs(f(x_new))) # Calculate the error at the x_new
        
        if abs(x_new - x) < tol:
            return x_new, iterations, errors
        
        x = x_new

# Define the index route
@app.route('/', methods=['GET', 'POST']) #serve the form on GET request and process the form on POST request
def index():
    root_bisection, iterations_bisection, errors_bisection = None, None, None # Initialize the variables
    root_newton, iterations_newton, errors_newton = None, None, None # None means no result
    plot_url = None

    if request.method == 'POST': # If the form is submitted
        function_str = request.form['function'] # Get the function from the form
        try:
            a = float(request.form['a'])
            b = float(request.form['b'])
            tol = float(request.form['tol'])
        except ValueError:
            return "Invalid numeric input" # If the input is not numeric

        x = sp.symbols('x') # Define the symbol x

        try:
            expr = sp.sympify(function_str) # Parse the function
            f = sp.lambdify(x, expr, 'numpy') # Convert the sympy expression to a numpy-ready function
            f_prime = sp.lambdify(x, sp.diff(expr, x), 'numpy') # Compute the derivative of the function
        except Exception as e:
            return f"Error parsing function: {e}"

        # Solve the root-finding problem
        try:
            root_bisection, iterations_bisection, errors_bisection = bisection_method(f, a, b, tol)
            root_newton, iterations_newton, errors_newton = newton_method(f, f_prime, (a + b) / 2.0, tol)
        except Exception as e:
            return f"Error solving root-finding problem: {e}"

        # Plot the convergence graph
        if root_bisection is not None and root_newton is not None:
            plt.figure()
            plt.plot(range(1, iterations_bisection + 1), errors_bisection, label='Bisection')
            plt.plot(range(1, iterations_newton + 1), errors_newton, label='Newton')
            plt.xlabel('Iterations')
            plt.ylabel('Error')
            plt.title('Convergence Graph')
            plt.legend()
            
            img = io.BytesIO() # Create a bytes buffer for saving the plot
            plt.savefig(img, format='png') 
            img.seek(0) # Move the cursor to the beginning of the file
            plot_url = base64.b64encode(img.getvalue()).decode()
            plt.close() 

        # Render the template with the results
        return render_template('index.html', root_bisection=root_bisection, iterations_bisection=iterations_bisection,
                               root_newton=root_newton, iterations_newton=iterations_newton, plot_url=plot_url)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=21002 , debug=True) 
