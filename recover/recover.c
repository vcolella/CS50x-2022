#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;
const short BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    // If number of arguments is incorrect
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");

    if (file == NULL)
    {
        printf("Image could not be read.\n");
        return 1;
    }

    BYTE *buffer = malloc(sizeof(BYTE) * BLOCK_SIZE);
    short counter = 0;
    char file_name[8];
    // sprintf(file_name, "%03d.jpg", counter);
    FILE *output = NULL;

    // Reading loop
    while (fread(buffer, 1, BLOCK_SIZE, file) == BLOCK_SIZE)
    {
        // If we find a JPG header
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] >> 4) == 0x0e)
        {
            // If an output file was already opened
            if (output != NULL)
            {
                fclose(output);
                counter++;
            }
            sprintf(file_name, "%03d.jpg", counter);
            output = fopen(file_name, "w");
        }

        if (output != NULL)
        {
            fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, output);
        }
    }
    // Freeing stuff
    free(buffer);
    fclose(file);
    fclose(output);
}