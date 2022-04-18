from cs50 import get_int

while True:
    height = get_int("Height: ")
    if height > 0 and height < 9:
        break

spaces = height - 1

for i in range(height):
    print(f" " * spaces + "#" * (i + 1) + "  " + "#" * (i + 1))
    spaces -= 1
