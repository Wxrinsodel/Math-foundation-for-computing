import numpy as np

def generate_diagonally_dominant_matrix(n):
    # Generate a random matrix
    A = np.random.rand(n, n)
    
    # Make it diagonally dominant
    for i in range(n):
        A[i, i] = np.sum(np.abs(A[i, :])) + 1  # Ensure diagonal dominance
    
    # Generate exact solution
    x_exact = np.random.rand(n)
    
    # Compute b such that A @ x_exact = b
    b = A @ x_exact
    
    return A, b, x_exact

# Example usage
n = 5
A, b, x_exact = generate_diagonally_dominant_matrix(n)
print("A:\n", A)
print("b:\n", b)
print("x_exact:\n", x_exact)