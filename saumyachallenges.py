#funcy.py
import time

# terminal print commands
ANSI_CLEAR_SCREEN = u"\u001B[2J"
ANSI_HOME_CURSOR = u"\u001B[0;0H\u001B[2"
OCEAN_COLOR = u"\u001B[44m\u001B[2D"
SHIP_COLOR = u"\u001B[32m\u001B[2D"
RESET_COLOR = u"\u001B[0m\u001B[2D"

def ocean_print():
    # print ocean
    print(ANSI_CLEAR_SCREEN, ANSI_HOME_CURSOR)
    print("\n\n\n\n")
    print(OCEAN_COLOR + "  " * 35)


# print ship with colors and leading spaces
def ship_print(position):
    print(ANSI_HOME_CURSOR)
    print(RESET_COLOR)
    sp = " " * position
    print(sp + "    |\   ")
    print(sp + "    |/   ")
    print(SHIP_COLOR, end="")
    print(sp + "\__ |__/ ")
    print(sp + " \____/  ")
    print(RESET_COLOR)


# ship function, iterface into this file
def ship():
    # only need to print ocean once
    ocean_print()

    # loop control variables
    start = 0  # start at zero
    distance = 60  # how many times to repeat
    step = 2  # count by 2

    # loop purpose is to animate ship sailing
    for position in range(start, distance, step):
        ship_print(position)  # call to function with parameter
        time.sleep(.1)




#christmastree
def christmastree(n):
    for i in range(n):
        for j in range(n-i):
            print(' ', end=' ')
        for k in range(2*i+1):
            print('*',end=' ')
        print(' ')


def trunk(n):
    for i in range(n):
        for j in range(n-6):
            print(' ', end = ' ')
        print('* * *')
    # Input and Function Call
row = int(input('Enter number of rows: '))

christmastree(row)
trunk (row)

















# Write a python program to print a 3x3 formatted matrix as shown below, using lists and nested loops.
# Make note of 2d array, loop/iteration and zero based counting.
# matrix = [ [1,2,3],[4,5,6],[7,8,9] ] #write a function to output the formatted matrix :
# 1 2 3
# 4 5 6
# 7 8 9

matrix = [ [1,2,3],[4,5,6],[7,8,9] ]

# print each sublist in new row
# for row in matrix:
#   print (row, sep=',')
# a = matrix[0
# print(a)

a = matrix[0][0], matrix[0][1], matrix[0][2]
b = matrix[1][0], matrix[1][1], matrix[1][2]
c = matrix[2][0], matrix[2][1], matrix[2][2]
print(*a, sep=" ")
print(*b, sep=" ")
print(*c, sep=" ")



# swaps numbers regardless of value
def swap1(age1,age2):
    temp = age1
    age1 = age2
    age2 = temp
    print("Swap 1 Result:")
    return age1,age2

#returns numbers lowest to highest
def swap2(a, b):
    if a > b:
        b, a = a, b
    print("Swap 2 Result:")
    return a, b

# returns numbers lowest to highest
def swap3(age1, age2):
    if age1 > age2:
        print ("Swap 3 Result:")
        return(age2, age1)
    else:
        print ("Swap 3 Result:")
        return(age1, age2)

# tests
print(16,20)
print(9.134,4)
print(swap1(16, 20))
print(swap1(9.134, 4))
print(swap2(16,20))
print(swap2(9.134, 4))
print(swap3(16,20))
print(swap3(9.134, 4))