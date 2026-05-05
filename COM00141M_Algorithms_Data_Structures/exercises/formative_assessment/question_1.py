# import pytest

"""
When you start to learn touch typing, you only practice on a subset of keys on the keyboard.
Quite often the exercises consist of repeating sequences of this subset of keys, however, most
of the time these sequences do not have a meaning or do not even represent an existing word.
To make the exercises more interesting and engaging, we want to take a text from a book and
keep only the words from that text that contains only letters from a subset of keys.

Write a function extract_text(text, keys) that returns a string containing only words
from the string text that are only composed of letters from the string keys. For simplicity we
make the following assumptions:
    • The string text contains only alphabet letters and blank spaces, no numbers or
    punctuation,
    • the string keys is not empty,
    • the parameters provided will satisfy the two previous statements, and there is no need
    to check the inputs.

In addition, the function must meet the following requirements:
    • each word in the returned string is separated by a single blank space,
    • the returned string does not start or end with a blank space,
    • the function should be case insensitive, that is the function should return the string
    ’Reader’ if the input text is ’Reader’ and the keys parameter is ’ArEdz’,
    • if the parameter text is an empty string, the function returns an empty string.
"""


def extract_text(text: str, keys: str) -> str:
    ret: list[str] = []
    if not len(text) or not len(keys):
        return ""

    word: str = ""
    invalid = False
    for c in text:
        if not c.isspace() and c.lower() not in keys.lower():
            invalid = True
            continue

        if not c.isspace() and invalid:
            continue

        if not c.isspace():
            word += c
        else:
            if not invalid:
                ret.append(word)

            word = ""
            invalid = False

    if word != "" and not invalid:
        ret.append(word)

    return " ".join(ret)


# @pytest.mark.parametrize(
#     ("text", "keys", "expected"),
#     (
#         (
#             "The term conda is not recognised as the name of a",
#             "theAsORin",
#             "The is not as the a"
#         ),
#         ("", "theAsORin", ""),
#         ("Reader", "ArEdz", "Reader"),
#         ("ab", "a", "")
#     )
# )
# def test_extract_keys(text, keys, expected):
#     assert extract_text(text, keys) == expected
