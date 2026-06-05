# 3. Number Guessing Game
# Build a game where:
# - computer selects a random number
# - user guesses the number
# - program gives hints: too high or too low
# - user gets limited attempts
# - invalid input is handled safely

import random
n = random.randint(1,100)

while (True):
    user = int(input("Enter your guess:"))
    if (user == n):
        print(f"Correct, you found the number: {n}")
        break
    elif(user > n):
        print("Your guess was higher than the number. Try again.")
    elif(user < n):
        print("Your guess was lower than the number.")
    elif(user == 0):
        print("Thank you for playing the game.")
        break


