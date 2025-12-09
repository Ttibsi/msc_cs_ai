"""
Exercise 1:
We want to create a function sum_from_file(filename) that calculate the sum of
all int contained in the text file filename. The format of the text file is as follow, a series
of int separated by a space spanning several lines as shown below. In the example below
the returned value should be 100.
    1 30 4 5
    8 12 19 1
    5 5 10

1 - It is sometime useful to decompose the problem into smaller problem. In this case it
    would be useful to have a function sum_numbers(a_string) that calculates and
    returns the sum of all numbers contained in the string a_string. The format of the
    string is a series of int separated by a space

2 - The function should raise a ValueError when the format of the file is not as
described

3 - The function should return None if the file passed in parameters does not exist

4 - Write the docstring (python documentation) for this function
"""

def sum_numbers(a_string: str) -> int:
    if " " not in a_string:
        raise ValueError

    nums: list[int] = [int(n) for n in a_string.split(" ")]
    return sum(nums)


def sum_from_file(filename: str) -> int | None:
    """ Sums up the contents of a file of lines of ints

    Args:
        filename: The file to sum up

    Returns:
        total sum of all numbers in the file, None if the filename is empty
    """

    if not filename:
        return None

    total = 0
    with open(filename) as  f:
        lines = f.readlines()

        for line in lines:
            try:
                total += sum_numbers(line)
            except ValueError:
                ...
            
    return total


"""
Exercise 2:
The aim of this exercise is to compute the score of an athlete in a given track event. We
need to convert a time in seconds into points. The formula is:
    points = a(b ― time)c

Where time is the time in seconds of the athlete for that event. a, b and c are parameters
that vary depending on the event (see Table 1). The value of points must be rounded down
to a whole number after applying the respective formula (e.g. 499.999 points becomes 499).
If the value of points is less than 0, then 0 should be returned instead

Write a function track_points(time, eventParameters) which takes a float
parameter time representing the athlete's time in seconds, and a tuple containing the
event's parameters (a, b, c) in that order. The method returns an int representing the
points scored for that event using Equation provided earlier.
The method raises a ValueError if eventParameters does not have exactly 3 values.
"""

def track_points(time: float, eventParameters: tuple[float, float, float]) -> int:
    if len(eventParameters) != 3:
        raise ValueError("Provide exactly 3 event parameters")

    a, b, c = eventParameters
    return int(a * (b - time) * c)


"""
Exercise 3:
Write a function rasterise(list_1D, width) that transforms a 1D list passed as
parameter into a 2D list, where each sub-list have width elements. If the length of the 1D
list is not a multiple of width, the function must raise a BufferError with an
appropriate error message. If width is less than 1, the function must raise a ValueError
with an appropriate error message.
"""

def rasterise(list_1D: list[int], width: int) -> list[list[int]]:
    if len(list_1D) % width:
        raise BufferError(f"List length {len(list_1D)} is not a multiple of {width}")
    if width < 1:
        raise ValueError("Please provide a valid width")

    ret = []
    temp = []
    for idx, i in enumerate(list_1D, start=1):
        temp.append(i)

        if not idx % width:
            ret.append(temp)
            temp = []

    return ret
