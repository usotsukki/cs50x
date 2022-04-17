#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cs50.h>
#include <ctype.h>

int main(int argc, char *argv[])
{
    if (argc !=2)
        {
            printf ("Usage: ./substitution KEY\n");
            return 1;
        }
    if (strlen(argv[1]) !=26)
        {
            printf ("Usage: ./substitution KEY\n");
            return 1;
        }
    for (int i = 0; i < 25; i++)
    if (!isalpha(argv[1][i]))
        {
            printf ("Usage: ./substitution KEY\n");
            return 1;
        }
    string p = get_string("plain text: ");
    printf("ciphertext: ");
    int len = strlen(p);
    for (int i = 0; i < len; i++)
    {
        char c = p[i];
        if (isalpha(c))
        {
            int ik = c - 65;
            char ck;

            if (islower(c))
                ck = (argv[1][ik-32])+32;
            else
                ck = argv[1][ik];

            printf("%c", ck);

        }
        else printf("%c", c);
    }
    printf("\n");
}