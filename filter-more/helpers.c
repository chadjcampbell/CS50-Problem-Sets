#include "helpers.h"
#include "math.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int average = round ((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][(width - 1) - j];
            image[i][(width - 1) - j] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sumred = 0;
            int sumgreen = 0;
            int sumblue = 0;
            float count = 0.0;
            for (int x = -1; x < 2; x++)
           {
               for (int y = -1; y < 2; y++)
               {
                   if (i + x >= 0 && j + y >= 0 && i + x < height && j + y < width)
                   {
                       sumred += copy[x + i][y + j].rgbtRed;
                       sumgreen += copy[x + i][y + j].rgbtGreen;
                       sumblue += copy[x + i][y + j].rgbtBlue;
                       count++;
                   }
               }
           }
        image[i][j].rgbtRed = round(sumred / count);
        image[i][j].rgbtGreen = round(sumgreen / count);
        image[i][j].rgbtBlue = round(sumblue / count);
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    double gx[3][3] = {{-1, 0, 1},
                       {-2, 0, 2},
                       {-1, 0, 1}};

    double gy[3][3] = {{-1, -2, -1},
                       {0, 0, 0},
                       {1, 2, 1}};

    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            double gxsumred = 0;
            double gysumred = 0;
            double gxsumgreen = 0;
            double gysumgreen = 0;
            double gxsumblue = 0;
            double gysumblue = 0;
            for (int x = -1, gmatrixi = 0; x < 2; x++, gmatrixi++)
           {
               for (int y = -1, gmatrixj = 0; y < 2; y++, gmatrixj++)
               {
                   if (i + x >= 0 && j + y >= 0 && i + x < height && j + y < width)
                   {
                       gxsumred += copy[x + i][y + j].rgbtRed * gx[gmatrixi][gmatrixj];
                       gysumred += copy[x + i][y + j].rgbtRed * gy[gmatrixi][gmatrixj];
                       gxsumgreen += copy[x + i][y + j].rgbtGreen * gx[gmatrixi][gmatrixj];
                       gysumgreen += copy[x + i][y + j].rgbtGreen * gy[gmatrixi][gmatrixj];
                       gxsumblue += copy[x + i][y + j].rgbtBlue * gx[gmatrixi][gmatrixj];
                       gysumblue += copy[x + i][y + j].rgbtBlue * gy[gmatrixi][gmatrixj];
                   }
               }
           }

        if (round(sqrt(pow(gxsumred, 2) + pow(gysumred, 2))) > 255)
            image[i][j].rgbtRed = 255;
        else
            image[i][j].rgbtRed = round(sqrt(pow(gxsumred, 2) + pow(gysumred, 2)));
        if (round(sqrt(pow(gxsumgreen, 2) + pow(gysumgreen, 2))) > 255)
            image[i][j].rgbtGreen = 255;
        else
            image[i][j].rgbtGreen = round(sqrt(pow(gxsumgreen, 2) + pow(gysumgreen, 2)));
        if (round(sqrt(pow(gxsumblue, 2) + pow(gysumblue, 2))) > 255)
            image[i][j].rgbtBlue = 255;
        else
            image[i][j].rgbtBlue = round(sqrt(pow(gxsumblue, 2) + pow(gysumblue, 2)));
        }
    }
    return;
}