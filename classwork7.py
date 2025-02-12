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


print("Matrix A:")
for row in A:
    print(row)
print("Exact solution x_exact:", x_exact)
print("Vector b:", b)

#1.b
def generate_initial_approximation(x_exact):
    # Add small random values to the exact solution
    return [x_exact[i] + random.uniform(-0.5, 0.5) for i in range(len(x_exact))]

x0 = generate_initial_approximation(x_exact)
print("Initial approximation x0:", x0)