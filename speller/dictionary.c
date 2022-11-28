// Implements a dictionary's functionality
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <math.h>
#include <stdlib.h>



#include <ctype.h>
#include <stdbool.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26 * LENGTH;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    for (node *tmp = table[hash(word)]; tmp != NULL; tmp = tmp->next)
    {
        if (strcasecmp(tmp->word, word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    return (toupper(word[0]) - 'A') * LENGTH + (strlen(word) - 1);

}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *f = fopen(dictionary, "r");
    if (f == NULL)
    {
        printf("Dictionary couldn't be openned\n");
        return false;
    }
    char buffer[LENGTH + 1];
    // Lets say we ignore the first node in the linked list being created
    while (fscanf(f, "%s\n", buffer) != EOF)
    {
        // Allocate new node
        node *n = malloc(sizeof(node));

        if (n == NULL)
        {
            printf("Couldn't allocate memory\n");
            return false;
        }

        strcpy(n->word, buffer);

        if (table[hash(buffer)] != NULL)
        {
            n->next = table[hash(buffer)];
        }
        else
        {
            n->next = NULL;
        }

        table[hash(buffer)] = n;

    }
    fclose(f);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    unsigned int words = 0;
    if (sizeof(table) > 0)
    {
        for (int i = 0; i < N; i++)
        {
            node *tmp = table[i];
            // Check if there's a word here
            if (tmp != NULL)
            {
                words++;
                while (tmp->next != NULL)
                {
                    tmp = tmp->next;
                    if (strstr(tmp->word, "\0"))
                    {
                        words++;
                    }
                }
            }
        }
    }
    return words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    // Runs through hashtable
    for (int i = 0; i < N; i++)
    {
        // Runs through linked list
        while (table[i] != NULL)
        {
            // Remembers the next node
            node *tmp = table[i]->next;
            free(table[i]);
            table[i] = tmp;
        }
    }
    return true;
}
