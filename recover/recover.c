#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

const int fatbytes = 512;

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    FILE *data = fopen(argv[1], "r");
    if (data == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }
    //Variables
    typedef uint8_t byte;
    byte buffer[fatbytes];
    int count = 0;
    char filename[8];
    FILE *img;
    //Read loop
    while (fread(buffer, sizeof(byte), fatbytes, data) == fatbytes)
    {
        //Beginning of JPG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (count == 0)
            {
                sprintf(filename, "%03i.jpg", count);
                img = fopen(filename, "w");
                fwrite(buffer, sizeof(byte), fatbytes, img);
                count++;
            }
            else
            {
                fclose(img);
                sprintf(filename, "%03i.jpg", count);
                img = fopen(filename, "w");
                fwrite(buffer, sizeof(byte), fatbytes, img);
                count++;

            }
        }
        else
        {
            if (count != 0)
            {
                fwrite(buffer, sizeof(byte), fatbytes, img);
            }
        }
    }
    fclose(img);
    fclose(data);
}