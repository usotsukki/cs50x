#include <stdio.h>
#include <cs50.h>
#include <math.h>
#include <string.h>
int main(void)
{
    string text = get_string("Text: ");

    int n = strlen(text);
    double sum_let=0;
    double sum_spaces=0;
    double sum_dots=0;
    for (int i = 0; i < n; i++)
    {
        int value = text[i];
        if (value==32) sum_spaces++;
        else if ((value>64&&value<91)||(value>96&&value<123)) sum_let++;
        else if (value==33 || value==46 || value==63) sum_dots++;
    }

    double l = sum_let/(sum_spaces+1)*100;
    double s = sum_dots/(sum_spaces+1)*100;
    double index = (0.0588*l)-(0.296*s)-15.8;
    int grade = round(index);

    if (grade>=1 && grade<=16) printf("Grade %i\n", grade);
    else if (grade<1) printf("Before Grade 1\n");
    else printf("Grade 16+\n");

    return 0;
}