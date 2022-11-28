#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Prototypes
string encrypt(string text, string key);
int check_key(string key);

int main(int argc, string argv[])
{
    // Checking number of arguments
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    // Checking key
    string key = argv[1];
    if (check_key(key) != 0)
    {
        return 1;

    }

    // Continues to encrytion
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: %s\n", encrypt(plaintext, key));

    return 0;
}

// Converts text to a cipher using given key
string encrypt(string text, string key)
{
    // Gives cipher same size as text
    string cipher = text;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        // Encrypts character keeping case
        if (islower(text[i]))
        {
            cipher[i] = tolower(key[text[i] - 97]);
        }
        else if (isupper(text[i]))
        {
            cipher[i] = toupper(key[text[i] - 65]);
        }
    }

    return cipher;
}

// Checks if key is valid
int check_key(string key)
{
    int n = strlen(key);

    // If key size is invalid
    if (n != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }


    for (int i = 0; i < n; i++)
    {
        // If key characters are invalid
        if (isalpha(key[i]) == 0)
        {
            printf("Key characters must be valid.\n");
            return 1;
        }
        else
        {
            // If key characters are not unique
            for (int j = 0; j < i; j++)
            {
                if (tolower(key[j]) == tolower(key[i]))
                {
                    printf("Key characters must be unique.\n");
                    return 1;
                }
            }
        }
    }
    return 0;
}