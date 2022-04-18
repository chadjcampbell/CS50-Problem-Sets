#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int only_digits(string clinput);

int main(int argc, string argv[])
{
    int key[26];
    string clinput = argv[1];

    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    int numtest = only_digits(clinput);
    if (numtest == 0 || strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    for (int i = 0, n = 26; i < n; i++)
    {
        key[i] = tolower(clinput[i]) - 97;
    }
    int keytotal = 0;
    for (int i = 0, n = 26; i < n; i++)
    {
        keytotal += key[i];
    }
    if (keytotal != 325)
    {
        printf("Key must contain 26 UNIQUE characters.\n");
        return 1;
    }
    for (int i = 0; i < 26; i++)
    {
        for (int j = i + 1; j < 26; j++)
        {
            if (key[i] == key[j])
            {
                printf("Key must contain 26 UNIQUE characters.\n");
                return 1;
            }
        }
    }
    string plaintext = get_string("plaintext:  ");
    printf("ciphertext: ");

    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        if (isalpha(plaintext[i]))
        {
            if (isupper(plaintext[i]))
            {
                plaintext[i] -= 65;
                int keynum = plaintext[i];
                char new = key[keynum];
                new += 65;
                printf("%c", new);
            }
            if (islower(plaintext[i]))
            {
                plaintext[i] -= 97;
                int keynum = plaintext[i];
                char new = key[keynum];
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
        clinput[i] = tolower(clinput[i]);
        if (isalpha(clinput[i]))
        {
            alldigits += 1;
        }
        else
        {
            alldigits = 0;
            break;
        }
    }
    return alldigits;
}