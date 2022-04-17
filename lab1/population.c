#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //Preparations

    int iterations = 0;
    int min_start_num = 9;
    int start_num = 0;
    int end_num = 0;
    char *prompt_start = "Start size: ";
    char *prompt_end = "End size: ";
    char *disp_iterations = "Years: ";

    //Prompt start

    do
    {
        start_num = get_int("%s", prompt_start);
    }
    while (start_num < min_start_num);

    //Prompt end

    do
    {
        end_num = get_int("%s", prompt_end);
    }
    while (end_num < start_num);

    //Calculations

    while (start_num < end_num)
    {
        start_num = start_num - start_num / 4 + start_num / 3;
        iterations++;
    }

    //Display output

    printf("%s%i\n", disp_iterations, iterations);
}