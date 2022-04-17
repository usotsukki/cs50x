#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cs50.h>
#include <ctype.h>

bool check_valid_key(string key);

int main(int argc, string argv[])
{
    if (argc!=2 || !check_valid_key(argv[1]))
        {
            printf ("Usage: ./caesar key");
            return 1;
        }
    int key = atoi(argv[1]);
    string p = get_string("plain text: ");
    printf("ciphertext: ");
    int len = strlen(p);
    for (int i = 0; i < len; i++)
    {
        char c = p[i];
        if (isalpha(c))
        {
        char m = 'A';
        if (islower(c))
            m = 'a';
        printf("%c", (c - m + key) % 26 + m);   //c[i]=p[i]+key;
        }
    else printf("%c", c);
    }
    printf("\n");
}
bool check_valid_key(string key)
{
    int len = strlen(key);
    for (int i = 0; i < len; i++)
    if (!isdigit(key[i]))
        return false;
    return true;
}