from cs50 import get_float

# prompt valid input
amount = 0
while True:
    amount = get_float("Change owed: ")
    if amount > 0:
        break

# calculations
cents = round(amount * 100)
coins = cents // 25 + cents % 25 // 10 + cents % 25 % 10 // 5 + cents % 25 % 10 % 5

# output
print(coins)