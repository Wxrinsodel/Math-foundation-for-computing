import random

#task 0

def generate_random_linear_system(size):
    # Generate random matrix A with integer values
    A = [[random.randint(-10, 10) for _ in range(size)] for _ in range(size)]
    
    # Generate solution vector x 
    x = [i + 1 for i in range(size)] # x = [1, 2, 3, ..., size]
    
    # Calculate right-hand side vector b = Ax
    b = [sum(A[i][j] * x[j] for j in range(size)) for i in range(size)] 
    
    return A, b, x 

# Test the function
size = 2
A, b, x = generate_random_linear_system(size)
print("Random Matrix A:")
for row in A:
    print(row)
print("Solution vector x:", x)
print("Right-hand side vector b:", b)

print("-------------------------------------------")


#task 1
def print_matrix(A, b, step):
    print(f"Step {step}:")
    for i in range(len(A)):
        print(A[i], "|", b[i])
    print()

def forward_elimination(A, b):
    n = len(A)
    for col in range(n):
        # Swap rows if pivot element is zero
        if A[col][col] == 0:
            for row in range(col + 1, n):
                if A[row][col] != 0:
                    A[col], A[row] = A[row], A[col]
                    b[col], b[row] = b[row], b[col]
                    print(f"Swapped row {col} with row {row} to avoid zero pivot.")
                    print_matrix(A, b, f"after swapping rows {col} and {row}")
                    break
        
        # Perform elimination
        for row in range(col + 1, n):
            if A[row][col] != 0:  # Avoid unnecessary calculations
                factor = A[row][col] / A[col][col]
                for k in range(col, n):
                    A[row][k] -= factor * A[col][k]
                b[row] -= factor * b[col]
        
        print_matrix(A, b, f"after eliminating column {col}")
    
    return A, b


print("Initial Matrix:")
print_matrix(A, b, "initial")
forward_elimination(A, b)
