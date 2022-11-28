#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height = 0;// Defines height

    // Loop to get acceptable height
    while (height < 1 || height > 8)
    {
        height = get_int("Height: ");
    }

    int spaces = height - 1; // Counter for spaces to print

    // main for loop for passing through levels
    for (int i = 1; i <= height; i++)
    {
        for (int j = 1; j <= spaces; j++)
        {
            printf(" ");
        }
        for (int j = 1; j <= i; j++)
        {
            printf("#");
        }
        printf("  ");
        for (int j = 1; j <= i; j++)
        {
            printf("#");
        }
        printf("\n"); // breakline
        spaces--; // spaces counter update
    }
}