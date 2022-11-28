#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

// Prototypes
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Get user input
    string input = get_string("Text: ");

    // Calculate parameters
    int words = count_words(input);
    float L = (float) count_letters(input) / words * 100;
    float S = (float) count_sentences(input) / words * 100;

    // Coleman-Liau Index formula
    float index = 0.0588 * L - 0.296 * S - 15.8;

    // Result printing
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %d\n", (int) round(index));
    }
}

int count_letters(string text)
{
    int letters = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (islower(text[i]) || isupper(text[i])) // If it's a letter
        {
            letters++;
        }
    }

    return letters;
}

int count_words(string text)
{
    int words = 0;
    bool was_end = false; // Marker for solving multiple spaces
    for (int i = 0, n = strlen(text); i <= n; i++)
    {
        if (islower(text[i]) == 0 && isupper(text[i]) == 0 && text[i] != '-' && text[i] != '\'') // If it's not a "letter"
        {
            if (!was_end)
            {
                words++;
            }
            was_end = true;
        }
        else
        {
            was_end = false;
        }
    }

    return words;

}

int count_sentences(string text)
{
    int sentences = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?') // If it's a sentence ending
        {
            sentences++;
        }
    }

    return sentences;

}
