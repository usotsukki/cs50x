#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
int compute_score(string word);
int main(void)
{
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    if (score1>score2) printf("Player 1 wins\n");
    else if (score2 > score1) printf("Player 2 wins\n");
    else printf("Tie\n");
}
int compute_score(string word) // TODO: Compute and return score for string
{
    int score_sum = 0;                                  //initialize sum above all
    int n = strlen(word);                               //initialize size of s

    for (int i = 0; i < n; i++)
    {
        if (islower(word[i]))
            word[i]=toupper(word[i]);                       // and there will be CAPS
        int char_value = word[i];                             // c to int
        score_sum += POINTS[char_value-65];                //presumably scores will auto addup into final sum
    }
    return score_sum;                           //return  int
}