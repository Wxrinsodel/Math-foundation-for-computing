import random

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
