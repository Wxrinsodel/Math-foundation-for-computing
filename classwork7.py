import random
import matplotlib.pyplot as plt

# 1.a) Generate diagonally dominant matrix and known solution
def generate_diagonally_dominant_matrix(n):
    A = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n): # Generate random values
            if i == j:
                A[i][j] = random.uniform(10, 20)  # Ensure diagonal dominance
            else:
                A[i][j] = random.uniform(-1, 1)
    return A


def generate_exact_solution(n):
    return [random.uniform(-10, 10) for _ in range(n)]


def compute_vector_b(A, x_exact):
    n = len(A)
    b = [0.0 for _ in range(n)]
    for i in range(n):
        for j in range(n):
            b[i] += A[i][j] * x_exact[j]
    return b

n = 5
A = generate_diagonally_dominant_matrix(n) 
x_exact = generate_exact_solution(n)
b = compute_vector_b(A, x_exact)

print("Matrix A:")
for row in A:
    print(row)
print("Exact solution x_exact:", x_exact)
print("Vector b:", b)

# 1.b) Generate initial approximation
def generate_initial_approximation(x_exact):
    return [x_exact[i] + random.uniform(-0.5, 0.5) for i in range(len(x_exact))]

x0 = generate_initial_approximation(x_exact)
print("Initial approximation x0:", x0)

# 1.c) Perform 10 Jacobi iterations
def jacobi_iteration(A, b, x0, max_iterations=10):
    n = len(A)
    x = x0.copy()
    for iteration in range(max_iterations):
        x_new = [0.0 for _ in range(n)] # Create a new vector
        for i in range(n):
            sigma = 0.0 # Compute the sum of the other terms
            for j in range(n):
                if j != i:
                    sigma += A[i][j] * x[j] # Add the term to the sum
            x_new[i] = (b[i] - sigma) / A[i][i]
        x = x_new
        print(f"Iteration {iteration + 1}: {x}") 
    return x

x_jacobi = jacobi_iteration(A, b, x0) # Perform 10 Jacobi iterations

# 1.e) Jacobi with stop condition
def jacobi_iteration_with_stop(A, b, x0, tolerance=1e-6, max_iterations=1000):
    n = len(A)
    x = x0.copy()
    error_history = []
    for iteration in range(max_iterations): # Iterate until max_iterations
        x_new = [0.0 for _ in range(n)]
        for i in range(n):
            sigma = 0.0
            for j in range(n):
                if j != i:
                    sigma += A[i][j] * x[j]
            x_new[i] = (b[i] - sigma) / A[i][i]
        
        error = max(abs(x_new[i] - x[i]) for i in range(n)) # Compute the error
        error_history.append(error) # Store the error
        if error < tolerance:  # Check if the error is below the tolerance
            print(f"Converged after {iteration + 1} iterations.")
            break
        
        x = x_new
        print(f"Iteration {iteration + 1}: {x}")
    return x, error_history

x_jacobi, jacobi_error_history = jacobi_iteration_with_stop(A, b, x0)

# 2.a) Gauss-Seidel iteration
def gauss_seidel_iteration(A, b, x0, tolerance=1e-6, max_iterations=1000):
    n = len(A)
    x = x0.copy()
    error_history = []
    for iteration in range(max_iterations):
        for i in range(n):
            sigma = 0.0
            for j in range(n):
                if j != i:
                    sigma += A[i][j] * x[j]
            x[i] = (b[i] - sigma) / A[i][i]
        
        error = max(abs((b[i] - sum(A[i][j] * x[j] for j in range(n))) / A[i][i]) for i in range(n))
        error_history.append(error)
        if error < tolerance:
            print(f"Converged after {iteration + 1} iterations.")
            break
        
        print(f"Iteration {iteration + 1}: {x}")
    return x, error_history

x_gauss_seidel, gauss_seidel_error_history = gauss_seidel_iteration(A, b, x0)

# 3) Plot convergence graphs
plt.figure(figsize=(10, 6))
plt.plot(jacobi_error_history, label='Jacobi Method')
plt.plot(gauss_seidel_error_history, label='Gauss-Seidel Method')
plt.xlabel('Iteration Number')
plt.ylabel('Error')
plt.yscale('log')
plt.title('Convergence of Jacobi and Gauss-Seidel Methods')
plt.legend()
plt.grid(True)
plt.show()

# 2.b) Gauss-Seidel with Hilbert matrix
def generate_hilbert_matrix(n):
    return [[1 / (i + j + 1) for j in range(n)] for i in range(n)]

# Generate Hilbert matrix, vector b, and initial approximation
H = generate_hilbert_matrix(n)
b_hilbert = [1.0 for _ in range(n)]
x0_hilbert = [random.uniform(-0.5, 0.5) for _ in range(n)]  # Initial approximation
x_hilbert_gauss_seidel, hilbert_gauss_seidel_error_history = gauss_seidel_iteration(H, b_hilbert, x0_hilbert)

print("Approximate solution (Gauss-Seidel with Hilbert matrix):", x_hilbert_gauss_seidel)