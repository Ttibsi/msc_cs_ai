from collections import Counter
import math
# import pytest

"""
Terni lapilli, also known as "Rota"
or "Tabla Lusoria", is an ancient Roman strategy game and is often considered the ancestor of
the modern Tic-Tac-Toe. It was played on a round board between two players, using three pieces
each. The board has eight "spokes" and a single middle place as shown in Figure 1a.

In this question, we represent the board as a list of integers, where 0 represents an empty
"spoke", 1 represents a piece of player 1, and 2 represents a piece of player 2. The index of an
element in the list represents the position of the piece on the board as shown in Figure 1a. For
example, the board shown in Figure 1b is represented by the list [0,0,2,1,1,0,1,2,2].

Implement a function compute_code(board) that takes a list of int representing a board
state and returns a code-number representation of the board as a single int. The computation
of the code-number value is given by Equation 1.
𝑖𝑖=8
𝑐𝑐𝑐𝑐𝑐𝑐𝑐𝑐(𝑆𝑆) = � 𝑝𝑝𝑖𝑖 3𝑖𝑖
𝑖𝑖=0
Equation 1
where 𝑆𝑆 is the state of the board, 𝑖𝑖 is the position on the board, and 𝑝𝑝𝑖𝑖 ∈ {0,1,2} is the value
associated with the piece at position 𝑖𝑖 on the board, 0 if the position is empty. For example, the
code-number for the board shown in Figure 1b is given below:

𝑐𝑐𝑐𝑐𝑐𝑐𝑐𝑐(𝑆𝑆) = 0 × 30 + 0 × 31 + 2 × 32 + 1 × 33 + 1 × 34 + 0 × 35 + 1 × 36 + 2 × 37 + 2 × 38
= 18351

Where 𝑆𝑆 is [0,0,2,1,1,0,1,2,2]. In addition, the function should return None if the list does not
contain exactly 9 elements and exactly 3 of each element from the set {0, 1, 2}.
"""


def compute_code(board: list[int]) -> int | None:
    # the function should return None if the list does not contain exactly 9 elements
    if len(board) != 9:
        return None

    # the function should return None if the list does not contain exactly 3 of
    # each element from the set {0, 1, 2}.
    counter = Counter(board)
    if any(x not in (0, 1, 2) for x in counter.keys()):
        return None

    ret: int = 0

    for idx, elem in enumerate(board):
        ret += (elem * math.pow(3, idx))

    return ret


# @pytest.mark.parametrize(
#     ("board", "expected"),
#     (
#         ([0, 0, 2, 1, 1, 0, 1, 2, 2], 18351),
#         ([0, 0, 0, 0, 0, 0, 0, 0, 0], 0),
#         ([123], None),
#         ([1, 2, 3, 4, 5, 6, 7, 8, 9], None),
#     )
# )
# def test_compute_code(board, expected):
#     assert compute_code(board) == expected
