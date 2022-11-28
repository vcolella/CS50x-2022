#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Getting input number
    long cardNumber = get_long("Number: ");

    // defining some variables
    int size = 0;
    string flag = "INVALID\n";

    // Checking number of digits
    long temp = cardNumber;
    while (temp != 0)
    {
        int digit = temp % 10;
        temp = temp / 10;
        size++;
    }

    // Checking flag
    temp = cardNumber;
    int lastDigit = 0;
    for (int b = 1; b <= size; b++)
    {
        int digit = temp % 10;
        temp = temp / 10;

        // if we're on the second to last digit
        if (b == size - 1)
        {
            // switch case for deciding on flag
            switch (temp % 10)
            {
                case 3 :
                    if (digit == 4 || digit == 7)
                    {
                        flag = "AMEX\n";
                    }
                    break;
                case 4 :
                    flag = "VISA\n";
                    break;
                case 5 :
                    if (digit >= 1 && digit <= 5)
                    {
                        flag = "MASTERCARD\n";
                    }
                    break;
            }
        }

    }


    if (size == 13 || size == 15 || size == 16)
    {
        int sum = 0;
        temp = cardNumber;


        // Luhn's algorithm
        for (int i = 1; i <= size; i++)
        {
            int digit = temp % 10;
            temp = temp / 10;

            // Checking every other digit starting from the second-to-last
            if (i % 2 == 0)
            {
                int prod = digit * 2;
                while (prod != 0)
                {
                    int digit2 = prod % 10;
                    prod = prod / 10;

                    sum = sum + digit2;
                }
            }
            else
            {
                sum = digit + sum;
            }
        }

        // Conclusion of the algo
        if (sum % 10 == 0)
        {
            printf("%s", flag);
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }


}