import calendar
import string

def ex_one():
    multiplierStr = input("Enter a number: ")
    if multiplierStr not in string.digits:
        raise ValueError("I can't make a times table out of that")

    multiplier = int(multiplierStr)
    for i in range(0, 10, 1):
        print(f"{i} times {multiplier} is {i*multiplier:2}")


def ex_two():
    heightStr = input("Enter a number: ")
    height = int(heightStr)
    for i in range(1, height+1):
        print(f"{' ' * (height - i)}{'*'*i}")

    for i in range(height-1, 0, -1):
        print(f"{' ' * (height - i)}{'*'*i}")

def ex_three():
    yearStr = input("Enter a number: ")
    monthStr = input("Enter a number: ")
    year = int(yearStr)
    month = int(monthStr)

    cal = calendar.monthcalendar(year, month)
    for i in cal:
        for j in i:
            if j == 0:
                print("    ", end="")
            else:
                print(f" {j:2} ", end="")
        print("")

ex_three()

