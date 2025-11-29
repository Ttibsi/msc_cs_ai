import copy

def ispalindrome(word: str) -> bool:
    """
    Write a recursive function ispalindrome(word) that returns true if the string word is a
    palindrome, false otherwise. You can start with an implementation that does not deal with
    punctuation, and then refactor your code to consider punctuation.
    """

    if not word[0].isalpha():
        word = word[1:]

    if not word[-1].isalpha():
        word = word[:-1]

    if len(word) > 2:
        if ispalindrome(word[1:-1]):
            return word[0] == word[-1]

    return word[0] == word[-1]


def rec_sum(numbers: list[int]) -> int:
    """
    To compute the sum of all elements in a list, you can use the built-in function sum.
        For example:
        >>> sum([1,2,3,4])
        10
        >>> sum([])
        0
    Write a recursive function rec_sum(numbers) that take a list of integers as a parameter
    and returns the sum of all the elements in the list. The function should return 0 if the list is
    empty.
    """

    if len(numbers):
        return rec_sum(numbers[1:]) + numbers[0]
    else:
        return 0


def sum_digits(num: int) -> int:
    """
    During week 3, we implemented the function sum_digits(number) to calculate and
    return the sum of digits of a given whole number (int) given as parameter. For example,
        >>> print(sum_digits(1234))
        10
    At the time we used loops in our implementation. This time you must use recursion. In
    addition, you are not allowed to convert the int into a list or a string.
    """

    return (num % 10) + sum_digits(num // 10) if num else 0


def flatten(mlist: list[list[int]]) -> list[int]:
    """
    Write a recursive function flatten(mlist) where mlist is a multidimensional list that
    returns all the element from mlist into a one-dimensional list. Note, empty lists are
    ignored. For examples:
    """

    flat_list = []
    for elem in mlist:
        if isinstance(elem, list):
            flat_list += flatten(elem)
        else:
            flat_list.append(elem)
    return flat_list


def merge(list_a, list_b):
    """
    Write a recursive function merge(sorted_listA, sorted_listB) that merges the
    two sorted lists into a single sorted list and returns it. The two parameters are list of
    comparable objects that are sorted in ascending order. For example, the lists contain only
    strings, or the lists contain only numbers. Neither of the two lists in the parameters must be
    modified
    """

    inner_a = copy.deepcopy(list_a)
    inner_b = copy.deepcopy(list_b)

    def inner(a,b,mem):
        if not a:
            mem.extend(b)
            return mem
        elif not b:
            mem.extend(a)
            return mem

        if a[0] < b[0]:
            pop = a[0]
            a = a[1:]
            mem.append(pop)
            out = inner(a, b, mem)
            return out
        else:
            pop = b[0]
            b = b[1:]
            mem.append(pop)
            out = inner(a, b, mem)
            return out

    out = inner(inner_a, inner_b, [])
    return out


def iselfish(word: str) -> bool:
    """
    A word is considered elfish if it contains all the letters: e, l, and f in it, in any order. For
    example, we would say that the following words are elfish: whiteleaf, tasteful, unfriendly,
    and waffles, because they each contain those letters 

    Write a predicate function called iselfish(word) that, given a word, tells us if
    that word is elfish or not. The function must be recursive
    """

    check = ['e', 'l', 'f']
    def inner(word, idx, mem):
        if idx == len(word):
            return mem

        if word[idx] in check:
            mem.append(1)
        else:
            mem.append(0)

        return inner(word, idx + 1, mem)

    return sum(inner(word, 0, [])) >= 3

        
def something_ish(pattern: str, word: str) -> bool:
    """
    Write something_ish(pattern, word)a more generalized predicate function
    that, given two words, returns true if all the letters of pattern are contained in
    word
    """

    def inner(word, idx, mem):
        if idx == len(word):
            return mem

        if word[idx] in pattern:
            mem.append(1)
        else:
            mem.append(0)

        return inner(word, idx + 1, mem)

    return sum(inner(word, 0, [])) >= 3
