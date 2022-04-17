#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    // prompt valid intput
    float amount;
    do
    amount = get_float("Change owed: ");
    while (amount < 0);

    // calculations
    int cents = round(amount * 100);
    int coins = cents / 25 + cents % 25 / 10 + cents % 25 % 10 / 5 + cents % 25 % 10 % 5;

    // output
    printf("%i\n",coins);
}