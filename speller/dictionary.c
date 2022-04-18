// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <string.h>
#include <cs50.h>
#include <math.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 150000;
int count = 0;
int col = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int hashnum = hash(word);
    node *cursor = table[hashnum];
    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        else
        {
            cursor = cursor->next;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int hashnum = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        char lower = tolower(word[i]);
        hashnum += (int)lower * 293 * i * i;
    }
    if (hashnum > N)
    {
        return (hashnum % N);
    }
    else
    {
        return hashnum;
    }

}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    char dicword[LENGTH + 1];
    FILE *input = fopen(dictionary, "r");
    if (input == NULL)
    {
        return false;
    }
    while (fscanf(input, "%s", dicword) != EOF)
    {
        node *n = malloc(sizeof(node));
        strcpy(n->word, dicword);
        n->next = NULL;
        int hashnum = hash(n->word);
        if (table[hashnum] == NULL)
        {
            table[hashnum] = n;
        }
        else
        {
            col++;
            n->next = table[hashnum];
            table[hashnum] = n;
        }
        count++;
    }
    fclose(input);
    printf("Collisions:       %i", col);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    node *cursor = NULL;
    node *temp = NULL;
    for (int i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            cursor = table[i];
            while (cursor != NULL)
            {
                temp = cursor;
                cursor = cursor->next;
                free(temp);
            }
        }
    }
    return true;
}
