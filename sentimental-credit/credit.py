# replicates credit.c

import re


def checksum(numberS):
    # Implements Luhn's algorithm
    number = int(numberS)
    sum = 0
    for i in range(1, len(numberS) + 1):
        digit = number % 10
        number = int(number / 10)

        # Checking every other digit starting from the second-to-last
        if i % 2 == 0:
            prod = digit * 2
            while prod != 0:
                digit2 = prod % 10
                prod = int(prod / 10)

                sum = sum + digit2
        else:
            sum = sum + digit

    # Conclusion of the algo
    if sum % 10 == 0:
        return True
    else:
        return False


def main():
    # Card number
    card = input("Number: ")

    # Check number of digits
    hint = ''

    # Checking if it looks like a credit card from any known flag
    if re.search("^((?:34|37)\d{13})$", card) is None:
        if re.search("^((?:51|52|53|54|55)\d{14})$", card) is None:
            if re.search("^((?:4)(?:\d{12}|\d{15}))$", card) is None:
                print("INVALID")
                return -1
            else:
                hint = "VISA"
        else:
            hint = "MASTERCARD"
    else:
        hint = "AMEX"

    if checksum(card):
        print(hint)
        return 0
    else:
        print("INVALID")
        return 1


if __name__ == "__main__":
    main()