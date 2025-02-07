import matplotlib.pyplot as plt
import numpy as np

def f(x):
    return (x - 1) ** 3

def f_prime(x):
    return  3 * (x - 1) ** 2

def g(x, alpha=1.0):
    return x - alpha * f(x)  


def find_root_newton(f, f_prime, x0, num_iter):
    x_vals = []
    for _ in range(num_iter):
        x_vals.append(x0)  # Store the current estimate
        x0 = x0 - f(x0) / f_prime(x0)
    return x0, x_vals 


def find_root_bisect(f, a, b, num_iters):
    x_vals = []
    if f(a) * f(b) > 0: # Check if the interval is valid
        print("No root found")
        return None, None
    for _ in range(num_iters):
        c = (a + b) / 2
        x_vals.append(c) 
        if f(c) == 0:
            return c, x_vals
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return (a + b) / 2, x_vals



def find_root_fixed_point(g, x0, num_iter):
    x_vals = []
    for _ in range(num_iter):
        x_vals.append(x0)
        x0 = g(x0) 
    return x0, x_vals


a, b = 0, 3  # Interval for bisection
x0 = 0.5  # Starting point for Newton and Fixed-Point
num_iter = 50  
alpha = 1.0  
real_solution = 1  # Known root for comparison


root_newton, x_vals_newton = find_root_newton(f, f_prime, x0, num_iter)
root_bisect, x_vals_bisect = find_root_bisect(f, a, b, num_iter)
root_fixed, x_vals_fixed = find_root_fixed_point(lambda x: g(x, alpha), x0, num_iter) 


errors_newton = [abs(x - real_solution) for x in x_vals_newton] 
errors_bisect = [abs(x - real_solution) for x in x_vals_bisect] if x_vals_bisect else []
errors_fixed = [abs(x - real_solution) for x in x_vals_fixed]


# Plot results
plt.figure(figsize=(8, 6))
plt.yscale('log')
plt.xlabel("Iteration")
plt.ylabel("Error (log scale)")
plt.title("Error Convergence of Root-Finding Methods")


plt.plot(errors_newton, label="Newton's Method")
if errors_bisect:
    plt.plot(errors_bisect, label="Bisection Method")
plt.plot(errors_fixed, label="Fixed-Point Iteration")


plt.legend()
plt.grid()
plt.show()
