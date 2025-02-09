import random


N = 2

A = []

for i in range(N):
    row = []
    for j in range(N):
        row.append(random.randint(1,5))
    A.append(row)


real_solution = [random.randint(1,5) for i in range(N)] 


b = [0,0]
b[0] = A[0][0] * real_solution[0] + A[0][1] * real_solution[1]
b[1] = A[1][0] * real_solution[0] + A[1][1] * real_solution[1]


print(f"Matrix is {A}\nRighthand side is {b}")


solved = False
while not solved:
    x =[]
    for i in range(N):
        x.append(int(input(f"Enter x{i}: ")))
        print(f"You proposed the solution: {x}")

        test1 = A[0][0] * x[0] + A[0][1] * x[1]
        test2 = A[1][0] * x[0] + A[1][1] * x[1]

        if test1 == b[0] and test2 == b[1]:
            print("You solved it!")
            solved = True
        else:
            print(f"Incorrext. Try again. First row error: ",{test1} - b[0], "Second row error: ", {test2} - b[1])

            