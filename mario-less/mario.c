#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int dl;
    int h;
    do
    {
        h = get_int("Size: ");
    }
    while (h < 1 || h > 8);
    dl = h - 1;
    for (int r = 0; r < h; r++)
    {
        for (int d = 0; d < dl; d++)
        {
            printf(" ");
        }
        dl--;
        printf("#");
        for (int c = 0; c < r; c++)
        {
            printf("#");
        }
        printf("\n");
    }
}