#!/usr/bin/env python3

"""
Dice Rolling Functions
Author: Justin Hammel
Description: Functions that format dice roll command and generate random numbers
            corresponding to requested dice roll.
            Uses the random library to generate a pseudo-random number based on
            the number of sides on the dice. Function expects 2 ints to be passed
            from the user.
"""

"""External library imports"""

# pseudo-random number generation
import random

"""
Uses the random library to generate a pseudo-random number based on
the number of sides on the dice passed to the function. Function expects 1 int
as input for the die roll. Can be used on it's own to generate a random die
roll, or in combination with dieSum to tally multiple rolls.
"""
def dieRoller(sides):
    # pseudo-random number generation, uncomment if not called in other script
    # import random
    result = random.randint(1, sides)
    print(f"Your random number is {result} on a {sides} sided die")
    return result

"""
Function works with the dieRoller() function to tally the results of a die roll.
The number of rolls and the type of die are passed as ints. The int for die type
is passed tot he dieRoller() function to get a random number. Returns an int
that is the sum of the rolls.
"""
def dieSum(qty, sides):
    sum = 0
    for i in range(qty):
        sum = sum + dieRoller(sides)
    return sum
"""
Formatting function for the dieRoller(). Expects input as a string in the
form !rollxdy, where x and y are integers. This will return a list containing
2 integer values with formatted_roll[0] = qty and formatted_roll[1] = sides
"""
def rollFormatter(command):
    roll = []
    formatted_roll = []
    ## strip apart the string to get just the qty and side for the dice
    ## command enters as a string, will convert into list to parse
    for i in list(command.lower()):
        if i.isnumeric():    # discard ! and roll portion of string
            roll.append(i)  # roll list is numbers and a 'd' in the middle
        elif i == 'd':
            roll.append(i)
    ## join the list into a string, then split at the 'd' into 2 list items
    formatted_roll = "".join(roll).split("d")
    ## now the 2 list items can be split off to variables
    return formatted_roll
"""
Main control for dice rolling function. Takes in the string command <!rollxdy>
and will return the sum of the die roll.
"""
def dieMain(user_command):
    """ Called at runtime"""
    # user_command = input("Insert command in the form !rollxdy\n").lower()
    roll_nums = rollFormatter(user_command)
    print(roll_nums)
    f_qty = int(roll_nums[0])
    f_sides = int(roll_nums[1])
    print(f"You want to roll {f_qty}d{f_sides}")
    roll_result = dieSum(f_qty, f_sides)
    print(f"Final result is {roll_result}")
    return roll_result

if __name__ == "__main__":
    main()
