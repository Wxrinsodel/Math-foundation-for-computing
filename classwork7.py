import random

def generate_diagonally_dominant_matrix(n):
    # Generate a random n x n matrix with diagonal dominance
    A = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                A[i][j] = random.uniform(10, 20)  # Ensure diagonal dominance
            else:
                A[i][j] = random.uniform(-1, 1)
    return A

def generate_exact_solution(n):
    # Generate a random exact solution vector
    return [random.uniform(-10, 10) for _ in range(n)]

def compute_vector_b(A, x_exact):
    # Compute b = A * x_exact
    n = len(A)
    b = [0.0 for _ in range(n)]
    for i in range(n):
        for j in range(n):
            b[i] += A[i][j] * x_exact[j] # Compute the dot product
    return b

n = 2
A = generate_diagonally_dominant_matrix(n)
x_exact = generate_exact_solution(n)
b = compute_vector_b(A, x_exact)

# Print the generated data
print("Matrix A:")
for row in A:
    print(row)
print("Exact solution x_exact:", x_exact)
print("Vector b:", b)

#1.b
def generate_initial_approximation(x_exact):
    # Add small random values to the exact solution
    return [x_exact[i] + random.uniform(-0.5, 0.5) for i in range(len(x_exact))]

x0 = generate_initial_approximation(x_exact) # Generate initial approximation
print("Initial approximation x0:", x0)

#1.e
def jacobi_iteration_with_stop(A, b, x0, tolerance=1e-6, max_iterations=1000):
    n = len(A)
    x = x0.copy()
    for iteration in range(max_iterations):
        x_new = [0.0 for _ in range(n)]
        for i in range(n):
            sigma = 0.0
            for j in range(n):
                if j != i:
                    sigma += A[i][j] * x[j] # Compute the dot product
            x_new[i] = (b[i] - sigma) / A[i][i]
        
        # Check for convergence
        error = max(abs(x_new[i] - x[i]) for i in range(n))
        if error < tolerance:
            print(f"Converged after {iteration + 1} iterations.")
            break
        
        x = x_new
        print(f"Iteration {iteration + 1}: {x}") # Print intermediate results
    return x

x_jacobi = jacobi_iteration_with_stop(A, b, x0)

# Implementing Gauss-Seidel iteration algorithm
def gauss_seidel_iteration(A, b, x0, tolerance=1e-6, max_iterations=1000):
    n = len(A)
    x = x0.copy()
    for iteration in range(max_iterations): # Iterate until convergence
        for i in range(n):
            sigma = 0.0 # Compute the dot product
            for j in range(n):
                if j != i:
                    sigma += A[i][j] * x[j]
            x[i] = (b[i] - sigma) / A[i][i] # Update the current estimate
        
        # Check for convergence
        error = max(abs((b[i] - sum(A[i][j] * x[j] for j in range(n))) / A[i][i]) for i in range(n))
        if error < tolerance: # Convergence criterion
            print(f"Converged after {iteration + 1} iterations.")
            break
        
        print(f"Iteration {iteration + 1}: {x}") # Print intermediate results
    return x

x_gauss_seidel = gauss_seidel_iteration(A, b, x0)

# Test Gauss-Seidel algorithm with Hilbert matrix
def generate_hilbert_matrix(n):
    H = [[1 / (i + j + 1) for j in range(n)] for i in range(n)]
    return H

H = generate_hilbert_matrix(n)
b_hilbert = [1.0 for _ in range(n)] # All elements are 1
x0_hilbert = [random.uniform(-0.5, 0.5) for _ in range(n)] # Random initial approximation
x_hilbert_gauss_seidel = gauss_seidel_iteration(H, b_hilbert, x0_hilbert) # Run Gauss-Seidel

print("Approximate solution (Gauss-Seidel with Hilbert matrix):", x_hilbert_gauss_seidel)
