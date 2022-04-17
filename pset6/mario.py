from cs50 import get_int

# prompt valid input
height = 0;
while True:
    height = get_int("Height: ")
    if height in range(1, 9):
        break

# output loop
for i in range(1, height+1):
    for j in range(height, i, -1):
        print(" ", end="")
    for k in range(i):
        print("#", end="")
    print("  ", end="")
    for l in range(i):
        print("#", end="")
    print("")