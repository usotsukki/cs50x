#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // prompt valid input
    do
        int height = get_int("Height: ");
    while (height < 1 || height > 8);

    // output loop
    for (int i = 0; i < height; i++)
    {
        for (int j = height; j > i + 1; j--)
            printf(" ");
        for (int k = 0; k < i + 1; k++)
            printf("#");
        printf("  ");
        for (int l = 0; l < i + 1; l++)
            printf("#");
        printf("\n");
    }
}