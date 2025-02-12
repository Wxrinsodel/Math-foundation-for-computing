import random

# Task 0
def generate_random_linear_system(size):
    # Generate random matrix A with integer values
    A = [[random.randint(-10, 10) for _ in range(size)] for _ in range(size)]
    
    # Generate solution vector x 
    x = [i + 1 for i in range(size)] 
    
    # Calculate right-hand side vector b = Ax
    b = [sum(A[i][j] * x[j] for j in range(size)) for i in range(size)] 
    
    return A, b, x 

# Function to round numbers in a matrix or vector to the nearest hundredth
def round_to_hundredth(matrix_or_vector):
    if isinstance(matrix_or_vector[0], list):  # If it's a matrix
        return [[round(element, 2) for element in row] for row in matrix_or_vector]
    else:  # If it's a vector
        return [round(element, 2) for element in matrix_or_vector] # Round to the nearest hundredth

# Test the function
size = 3
A, b, x = generate_random_linear_system(size)
print("Random Matrix A:")
for row in A:
    print(row)
print("Solution vector x:", x)
print("Right-hand side vector b:", b)

print("-------------------------------------------")

# Store the original A and b for later comparison
original_A = [row.copy() for row in A]  # copy of the original matrix A
original_b = b.copy()  # copy of the original vector b

# Task 1, 2
def forward_gaussian_elimination(A, b):
    size = len(A) # Size of the matrix
    
    for i in range(size):
        # Swap rows if current pivot is zero
        if A[i][i] == 0:  # If the pivot is zero
            for k in range(i + 1, size):
                if A[k][i] != 0: # Find a row with non-zero pivot
                    A[i], A[k] = A[k], A[i]
                    b[i], b[k] = b[k], b[i] 
                    break
        
        # Eliminate elements below the current pivot
        for j in range(i + 1, size):
            if A[j][i] != 0:  # Skip if already zero
                factor = A[j][i] / A[i][i]
                for k in range(i, size):
                    A[j][k] -= factor * A[i][k]  # Update A[j][k]
                b[j] -= factor * b[i]
        
        # Print matrix after elimination step (rounded to hundredth)
        print(f"After elimination step {i + 1}:")
        rounded_A = round_to_hundredth(A) # Round the matrix to the nearest hundredth
        for row in rounded_A:
            print(row)
        rounded_b = round_to_hundredth(b) # Round the vector to the nearest hundredth
        print("Updated b vector:", rounded_b)
        print()
    
    return A, b

# Test with the generated system
A, b = forward_gaussian_elimination(A, b)

print("-------------------------------------------")

# Task 3
def backward_substitution(A, b): 
    size = len(A)
    x = [0] * size
    
    for i in range(size - 1, -1, -1):  # Iterate over rows in reverse order
        if A[i][i] == 0:
            raise ValueError("Division by zero encountered in backward substitution. The system may be singular.")
        x[i] = b[i] / A[i][i]
        for j in range(i):
            b[j] -= A[j][i] * x[i]  # Update right-hand side vector b
    
    # Round the solution vector x to the nearest hundredth
    x = round_to_hundredth(x)
    return x

# Test backward substitution
solution_x = backward_substitution(A, b)
print("Solution vector x found by backward substitution:", solution_x)

print("-------------------------------------------")

# Task 4
def test_solution(A, x, original_b):
    size = len(A) 
    b_calculated = [sum(A[i][j] * x[j] for j in range(size)) for i in range(size)] # Calculate b = Ax
    
    # Round the calculated b vector to the nearest hundredth
    b_calculated = round_to_hundredth(b_calculated)
    
    for i in range(size):
        if abs(b_calculated[i] - original_b[i]) > 1e-6:
            return False
    return True

# Test the solution
is_correct = test_solution(original_A, solution_x, original_b)
print("Is the solution correct?", is_correct)

# Task 5
def generate_hilbert_matrix(size):
    return [[1 / (i + j + 1) for j in range(size)] for i in range(size)]

def compute_residual(A, x, b):
    size = len(A) 
    b_calculated = [sum(A[i][j] * x[j] for j in range(size)) for i in range(size)]
    residual = [b_calculated[i] - b[i] for i in range(size)]  
    return round_to_hundredth(residual)

# Compare Gaussian elimination on normal random matrix vs. Hilbert matrix
def compare_gaussian_elimination(size):
    print("-------------------------------------------")
    print(f"Comparing Gaussian elimination for N = {size}")
    
    # Normal random matrix
    A_random, b_random, _ = generate_random_linear_system(size) 
    A_hilbert = generate_hilbert_matrix(size)
    b_hilbert = [sum(A_hilbert[i][j] * (j + 1) for j in range(size)) for i in range(size)]
    
    # Solve using Gaussian elimination
    print("\nSolving normal random matrix:")
    A_random_copy = [row.copy() for row in A_random]
    b_random_copy = b_random.copy() # Copy of the original vector b
    A_random_copy, b_random_copy = forward_gaussian_elimination(A_random_copy, b_random_copy) # Solve using Gaussian elimination
    x_random = backward_substitution(A_random_copy, b_random_copy) # Solve using backward substitution
    residual_random = compute_residual(A_random, x_random, b_random) # Calculate residual
    
    print("Solution for random matrix:", x_random)
    print("Residual (Ax - b) for random matrix:", residual_random)
    
    print("\nSolving Hilbert matrix:")
    A_hilbert_copy = [row.copy() for row in A_hilbert]
    b_hilbert_copy = b_hilbert.copy()
    A_hilbert_copy, b_hilbert_copy = forward_gaussian_elimination(A_hilbert_copy, b_hilbert_copy)
    x_hilbert = backward_substitution(A_hilbert_copy, b_hilbert_copy)
    residual_hilbert = compute_residual(A_hilbert, x_hilbert, b_hilbert)
    
    print("Solution for Hilbert matrix:", x_hilbert)
    print("Residual (Ax - b) for Hilbert matrix:", residual_hilbert)
    print("-------------------------------------------")

# Run comparisons for different sizes
for n in [1, 2, 3, 4, 5]:
    compare_gaussian_elimination(n)