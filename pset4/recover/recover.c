#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#define BLOCK_SIZE 512

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: recover infile\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[1];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    BYTE buffer[512];
    int imageCount = 0;

    char filename[8];
    FILE *outptr = NULL;

    while (true)
    {
        // read a block of the memory card image
        size_t bytesRead = fread(buffer, sizeof(BYTE), BLOCK_SIZE, inptr);

        // break out of the loop when we reach the end of the card image
        if (bytesRead == 0 && feof(inptr))
        {
            break;
        }

        // check if we found a JPEG
        bool containsJpegHeader = buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0;

        // if we found a yet another JPEG, we must close the previous file
        if (containsJpegHeader && outptr != NULL)
        {
            fclose(outptr);
            imageCount++;
        }

        // if we found a JPEG, we need to open the file for writing
        if (containsJpegHeader)
        {
            sprintf(filename, "%03i.jpg", imageCount);
            outptr = fopen(filename, "w");
        }

        // write anytime we have an open file
        if (outptr != NULL)
        {
            fwrite(buffer, sizeof(BYTE), bytesRead, outptr);
        }
    }

    // close last jpeg file
    fclose(outptr);

    // close infile
    fclose(inptr);

    // success
    return 0;
}
















/*
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>





int main(int argc, char *argv[])
{
    typedef uint8_t  BYTE;

    BYTE block[512];
    int imagenum = 000;
    char *infile = argv[1];
    int c=0;
    char outfile[10];
    sprintf(outfile, "%03d.jpg",c);



    //open the memory card
    // Remember filenames




    // Open input file
    FILE *inptr = fopen(infile, "r");

    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 4;
    }




    for (int i = 10000; i > 0; i--)
    {
        fread(&block, sizeof(block), 1, inptr);
        if ((block[0]==0xff)&&(block[1]==0xd8)&&(block[2]==0xff)&&((block[3]==0xe0)||(block[3]==0xe1)||(block[3]==0xe2)||(block[3]==0xe3)||(block[3]==0xe4)||(block[3]==0xe5)||(block[3]==0xe6)||(block[3]==0xe7)||(block[3]==0xe8)||(block[3]==0xe9)||(block[3]==0xea)||(block[3]==0xeb)||(block[3]==0xec)||(block[3]== 0xed)||(block[3]==0xee)||(block[3]==0xef)))
        {
            FILE *outptr = fopen(outfile, "w");
            fwrite(&block, sizeof(block),1 , outptr);
            fread(&block, sizeof(block), 1, inptr);
            if (!((block[0]==0xff)&&(block[1]==0xd8)&&(block[2]==0xff)&&((block[3]==0xe0)||(block[3]==0xe1)||(block[3]==0xe2)||(block[3]==0xe3)||(block[3]==0xe4)||(block[3]==0xe5)||(block[3]==0xe6)||(block[3]==0xe7)||(block[3]==0xe8)||(block[3]==0xe9)||(block[3]==0xea)||(block[3]==0xeb)||(block[3]==0xec)||(block[3]== 0xed)||(block[3]==0xee)||(block[3]==0xef))))
            {
                fwrite(&block, sizeof(block),1 , outptr);
            }

            fclose(outptr);
            c+=1;
            sprintf(outfile, "%03d.jpg",c);
        }
    }





    return 0;
}

    */
