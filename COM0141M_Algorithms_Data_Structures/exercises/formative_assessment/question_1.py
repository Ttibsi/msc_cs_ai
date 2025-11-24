import pytest

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

def extract_keys(text: str, keys: str) -> str:
    ret: str = ""
    words: list[str] = text.split()

    for word in words:
        not_found = False
        for c in word:
            if c.lower() not in keys.lower():
                not_found = True
                break

        if not not_found:
            ret += word + " "

    return ret[:-1]

@pytest.mark.parametrize(
    ("text", "keys", "expected"),
    (
        ("The term conda is not recognised as the name of a", "theAsORin", "The is not as the a"),
        ("", "theAsORin", ""),
        ("Reader", "ArEdz", "Reader"),
    )
)
def test_extract_keys(text, keys, expected):
    assert extract_keys(text, keys) == expected 
