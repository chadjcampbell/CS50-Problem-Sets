#include <cs50.h>
#include <stdio.h>

int checksum(long ccnum);
int card = 0;

int main(void)
{
    long ccnum = get_long("Number: ");

    int real = checksum(ccnum);

    if (real == 1 && card == 1)
    {
        printf("AMEX\n");
    }
    else if (real == 1 && card == 2)
    {
        printf("MASTERCARD\n");
    }
    else if (real == 1 && card == 3)
    {
        printf("VISA\n");
    }
    else
    {
        printf("INVALID\n");
    }

}

int checksum(long ccnum)
{
    long total = 0;
    int i = 0;
    if (ccnum < 1000000000000 || ccnum > 9999999999999999)
    {
        // If it is not 13 to 16 digits, it is invalid
        return 0;
    }
    else
    {
        for (i = 0; i < 16; i++)
        {
            long notdblnum = 0;
            long dblnum = 0;
            if (i % 2 == 0)
            {
                notdblnum = ccnum % 10;
                total += notdblnum;
            }
            else if (i % 2 == 1)
            {
                dblnum = ccnum % 10;
                dblnum *= 2;
                if (dblnum > 9)
                {
                    dblnum = dblnum - 9;
                }
                total += dblnum;
            }
            ccnum /=  10;
            // card type if statement, amex = 1, mc = 2, visa = 3
            if (ccnum == 34 || ccnum == 37)
            {
                card = 1;
            }
            if (ccnum > 50 && ccnum < 56)
            {
                card = 2;
            }
            if (ccnum == 4)
            {
                card = 3;
            }
        }
        if (total % 10 == 0)
        {
            return 1;
        }
        else
        {
            return 0;
        }
    }

}