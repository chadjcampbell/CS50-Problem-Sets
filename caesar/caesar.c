#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int only_digits(string clinput);

int main(int argc, string argv[])
{
    string clinput = argv[1];
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    int numtest = only_digits(clinput);
    if (numtest == 0)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    int rotate = atoi(argv[1]);
    string plaintext = get_string("plaintext:  ");
    printf("ciphertext: ");

    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        if (isalpha(plaintext[i]))
        {
            if (isupper(plaintext[i]))
            {
                plaintext[i] -= 65;
                char new = (plaintext[i] + rotate) % 26;
                new += 65;
                printf("%c", new);
            }
            if (islower(plaintext[i]))
            {
                plaintext[i] -= 97;
                char new = (plaintext[i] + rotate) % 26;
                new += 97;
                printf("%c", new);
            }
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    }

    printf("\n");
}

int only_digits(string clinput)
{
    int alldigits = 0;
    for (int i = 0, n = strlen(clinput); i < n; i++)
    {
        if (isdigit(clinput[i]) != 0)
        {
            alldigits += 1;
        }
        else
        {
            alldigits = 0;
        }
    }
    return alldigits;
}