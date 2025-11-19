
def order_price(quantity: int) -> int:
    """
    Exercise 1:
    A fruit company sells bananas for £3.00 a kilogram plus £4.99 per order for postage and
    packaging. If an order is over £50.00, the P&P is reduced by £1.50. Write a function
    order_price(quantity) that takes an int parameter quantity representing the number of
    kilo of bananas for the order, and returns the cost of the order in pence (as an int).
    """
    COST_PER_KG = 300

    raw_kg_cost = COST_PER_KG * quantity
    post_pack_cost = 499 if raw_kg_cost < 5000 else (499 - 150)

    return raw_kg_cost + post_pack_cost


def maximum_heart_rate(age: int) -> int:
    """
    Exercise 2:
    Write a function maximum_heart_rate(age) that takes the age of the person as
    parameter (an int) and returns the maximum heart rate for that person (as an int). The
    maximum heart rate is given by
    """

    return 208 - (0.7 * age)


def training_zone(age: int, rate: int) -> str:
    """
    Exercise 2.2:
    Write a second function training_zone(age, rate) that takes the age (as an int)
    and rate (the heart rate as an int) from the person as parameters and returns a string
    representing one of the four possible training zones of a person based on his or her age and
    training heart rate, rate. The zone is determined by comparing rate with the person's
    maximum heart rate m.
    """

    max_rate = maximum_heart_rate(age)
    if rate >= (0.9 * max_rate):
        return "Interval training"
    elif (0.7 * max_rate) <= rate <= (0.9 * max_rate):
        return "Threshold training"
    elif (0.5 * max_rate) <= rate <= (0.7 * max_rate):
        return "Aerobic training"
    else:
        return "Couch potato"


import string

def is_valid_password(
        password: str,
        min_length: int = 8,
        has_upper: bool = False,
        has_lower: bool = False,
        has_numeric: bool = False
)-> bool:
    """
    Exercise 3:
    Implement a function:
        is_valid_password(password, min_length, has_upper, has_lower, has_numeric)
    that takes the following parameters in that order:
    1. password: a password as a string
    2. has_upper: a Boolean. If True the password must contains at least one uppercase
    character
    3. has_lower: a Boolean. If True the password must contains at least one lowercase
    character
    4. has_numeric: a Boolean. If True the password must contains at least one numeric
    character
    The function returns True if the password meets the following criteria:
        1. at least min_length characters long,
        2. contains at least one uppercase character if has_upper is True
        3. contains at least one lowercase character if has_lower is True
        4. contains at least one numeric character if has_numeric is True
        5. Does not contain any special characters (that is non-alphanumeric like punctuation)

    In addition, by default the function checks that a password has both uppercase and lowercase,
    has a minimum length of 8 and contains at least one numeric character.
    """

    # 1. at least min_length characters long,
    if len(password) < min_length:
        return False

    # 2. contains at least one uppercase character if has_upper is True
    if has_upper and not any([c in string.ascii_uppercase for c in password]):
        return False

    # 3. contains at least one lowercase character if has_lower is True
    if has_lower and not any([c in string.ascii_lowercase for c in password]):
        return False

    # 4. contains at least one numeric character if has_numeric is True
    if has_numeric and not any([c in string.digits for c in password]):
        return False

    # 5. Does not contain any special characters (that is non-alphanumeric like punctuation)
    return password.isalnum()


def test_is_valid_password():
    """
    Design a series of tests using the assert statement to test the functionality of, and validity of
    your function
    """

    # Does this check the length correctly
    assert not is_valid_password("123", 5, False, False, False)
    assert is_valid_password("12345", 2, False, False, False)

    # Do we detect uppercase letters properly
    assert not is_valid_password("12345", 2, True, False, False)
    assert is_valid_password("A12345", 2, True, False, False)

    # Do we detect lowercase letters properly
    assert not is_valid_password("A12345", 2, False, True, False)
    assert is_valid_password("Aa12345", 2, False, True, False)

    # Do we detect numbers correctly
    assert not is_valid_password("ABCD", 2, False, False, True)
    assert is_valid_password("ABCD1234", 2, False, False, True)

    # Do we detect non-alphanumeric characters correctly
    assert not is_valid_password("AC-DC", 2, False, False, False)
    assert is_valid_password("ACDC", 2, False, False, False)


def sum_digits(num: int) -> int:
    """
    Exercise 4:
    Write a function sum_digits(number) to calculate and return the sum of the digits of a
    given whole number (an int NOT a string) given as a parameter

    Note: There are two ways to approach the problem, the simplest one is to convert the parameter
    number into a string within the function and then solve the problem one character at a time.
    However, if you want to challenge yourself, try to approach the problem differently by not
    converting the parameter number into any other data type.
    """

    total = 0
    while num:
        total += num % 10
        num //= 10

    return total


def pairwise_digits(number_a: str, number_b: str) -> str:
    """
    Exercise 5:
    Write a function pairwise_digits(number_a, number_b) that takes two whole
    numbers represented by strings (not int) as parameters and returns a binary string where a
    character 1 is used if the digits at the same index are the same, a 0 otherwise. If the two strings
    have different lengths, the output should be padded with 0s on the right-hand side to match the
    length of the longest string
    """

    ret = ""
    iterations = min(len(number_a), len(number_b))
    remaining = max(len(number_a), len(number_b))

    for i in range(iterations):
        if number_a[i] == number_b[i]:
            ret += "1"
            continue
        ret += "0"

    ret += "0" * (remaining - iterations)
    return ret

def test_pairwise_digits():
    parametrize = [
        ("1213", "2113", "0011"),
        ("1213", "1043567", "1001000"),
        ("12130", "121", "11100"),
    ]

    for lhs, rhs, ret in parametrize:
        assert pairwise_digits(lhs, rhs) == ret
