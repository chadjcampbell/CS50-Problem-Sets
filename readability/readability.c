#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");

    float lettercount = count_letters(text);

    float wordcount = count_words(text);

    float sentencecount = count_sentences(text);

    int index = round(0.0588 * ((lettercount / wordcount) * 100) - 0.296 * ((sentencecount / wordcount) * 100) - 15.8);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int count_letters(string text)
{
    int lettercount = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]) != 0)
        {
            lettercount++;
        }
    }
    return lettercount;
}

int count_words(string text)
{
    int wordcount = 1;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == 32)
        {
            wordcount++;
        }
    }
    return wordcount;
}

int count_sentences(string text)
{
    int sentencecount = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == 46 || text[i] == 33 || text[i] == 63)
        {
            sentencecount++;
        }
    }
    return sentencecount;
}
