# Replicates mario.c

from cs50 import get_int


def main():
    height = 0
    while height < 1 or height > 8:
        height = get_int("Height: ")
    # Counter for spaces to print
    spaces = height - 1
    # main for-loop for passing through levels
    for i in range(1, height + 1):
        for j in range(1, spaces + 1):
            print(" ", end='')
        for j in range(1, i + 1):
            print("#", end='')
        print("  ", end='')
        for j in range(1, i + 1):
            print("#", end='')
        # breakline
        print("\n", end='')
        # spaces counter update
        spaces -= 1


if __name__ == "__main__":
    main()