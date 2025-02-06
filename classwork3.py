import math


def fixed_point_iteration(g, x0, alpha=1.0, epsilon=1e-6, max_iterations=100):
    x = x0 
    count = 0 

    while True:
        x_new = x - alpha * (x - g(x))  # Update x using alpha
        count += 1  

        # If the number reaches the max iteration, stop
        if abs(x_new - x) < epsilon or count >= max_iterations:
            break
        
        x = x_new  # Move to the next guess

    return x_new, count


# Functions to test
def g1(x):
    return (alpha * (x ** 2 - x - 2 ) + x)  # Function 1

def g2(x):
   return (alpha * ( x + 3)) # Function 2


alphas = [-1 / 6, -1 / 3, -1 / 2, -2 / 3]  

# Try different step sizes on each function
for alpha in alphas:
    root1, iteration1 = fixed_point_iteration(g1, 1, alpha)
    print(f"Function g1 with α={alpha}: Root = {root1:.6f}, iteration = {iteration1}")

    root2, iteration2 = fixed_point_iteration(g2, 1.5, alpha)
    print(f"Function g2 with α={alpha}: Root = {root2:.6f}, iteration = {iteration2}")
