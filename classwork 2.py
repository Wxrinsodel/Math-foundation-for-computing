import math


#ensure that f(a) and f(b) have opposite signs

def find_valid_interval(f, a, b, step=0.5, max_attempts=50):
    """Expands the interval until f(a) and f(b) have opposite signs."""
    attempts = 0
    while f(a) * f(b) > 0 and attempts < max_attempts:
        a -= step
        b += step
        step *= 1.5  # increasing step size to speed up search
        attempts += 1

    if f(a) * f(b) > 0:
        raise ValueError("Could not find a valid interval with opposite signs.")

    return a, b


def bisection_method(f, a, b, tol=1e-6):
    """Finds a root of f in [a, b] using the bisection method."""
    if f(a) * f(b) > 0:
        return None  # No sign change, no root in this interval
    
    estimated_iterations = math.ceil(math.log((b - a) / tol) / math.log(2)) #mathceil = ปัดเศษขึ้น
    print(f"Estimated iterations needed: {estimated_iterations}")
    
    iterations = 0  # Track actual iterations
    while (b - a) / 2 > tol: # assume a < b
        m = (b + a) / 2 # find mid to get closer to 0
        if f(m) == 0:
            return m  # m is the root such that f(m) = 0
        elif f(a) * f(m) < 0:
            b = m  # Shrink interval from right.
        else:
            a = m # Shrink interval from left.

        iterations += 1 # loop until its converge
    
    print(f"Actual iterations performed: {iterations}")
    return (a + b) / 2


def find_all_roots(f, a, b, num_intervals=100, tol=1e-6):
    """Finds all roots of f in the interval [a, b] by subdividing the range."""
    step = (b - a) / num_intervals
    roots = []
    
    for i in range(num_intervals):
        x1, x2 = a + i * step, a + (i + 1) * step
        if f(x1) * f(x2) <= 0:  # Possible root in this interval
            root = bisection_method(f, x1, x2, tol)
            if root is not None and not any(abs(root - r) < tol for r in roots):
                roots.append(root)
    
    return roots


def func(x):
    return (x ** 4) + (3 * (x ** 3)) + (x ** 2) - (2 * x) - 0.5

a, b = -2, 1
tol = 1e-6 
roots = find_all_roots(func, a, b, num_intervals=100, tol=tol)
print("All approximate roots:", roots)
