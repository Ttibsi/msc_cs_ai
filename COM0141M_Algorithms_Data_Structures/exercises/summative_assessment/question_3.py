# Mars Rover Communication System
from __future__ import annotations
import copy
import itertools
import operator
import string
from enum import Enum
from typing import Callable
from typing import NamedTuple
from typing import TypeAlias

class Equality(Enum):
    """ Enumeration of match values for two Coordinates """
    NOMATCH = 1
    X_ONLY = 2
    Y_ONLY = 3


class Coordinate(NamedTuple):
    """ Coordinate NamedTuple for more structured data. """
    x: int
    y: int

    def equal(self, other: Coordinate | None) -> Equality:
        """ Compare two coordinate objects """
        if other is None:
            return Equality.NOMATCH
        if self.x == other.x:
            return Equality.X_ONLY
        if self.y == other.y:
            return Equality.Y_ONLY

        return Equality.NOMATCH


# Set up type aliases for clarity
# We here need to use the old syntax as gradescope runs in python3.10, not
# python3.12 as the brief states
Position_t: TypeAlias = tuple[Coordinate | None, Coordinate | None]
Grid_t: TypeAlias = list[list[str | None]]
func_t: TypeAlias = Callable[[int, int], int]


def batched(iterable: str, n: int) -> list[tuple[str, ...]]:
    """
    A clone of itertools.batched for python3.10 for gradescope compatibility

    Args:
    iterable: str - A string to iterate over
    n: int - The number of chars to include per iteration

    Returns:
    list[tuple[str, ...]] - a list of tuples of n length
    """

    ret = []
    temp = []

    for idx, c in enumerate(iterable, start=1):
        temp.append(c)

        if idx % n == 0:
            ret.append(tuple(temp))
            temp = []

    ret.append(tuple(temp))
    return ret


class CommunicationProtocol:
    _grid: Grid_t
    _mission_key: str

    def __init__(self, mission_key: str) -> None:
        """
        Construct a new CommunicationProtocol object

        Args:
        mission_key: str - Provide the initial mission key
        """

        self._mission_key = mission_key
        uppercase_key: str = mission_key.upper()
        valid_insertions = list(string.ascii_uppercase + string.digits)

        # Strip out repeated chars and chars not matching [A-Z0-9]
        stripped_key = ""
        for c in uppercase_key:
            # Check for existing presence first as stripped_key will have
            # less characters to check than all uppercase chars and digits
            if c not in stripped_key:
                if c in valid_insertions:
                    stripped_key += c
                    valid_insertions.remove(c)

        # start constructing the grid
        self._grid = self._create_grid(
            key=stripped_key,
            valid=valid_insertions
        )

    def _create_grid(self, *, key: str, valid: list[str]) -> Grid_t:
        """
        Required helper function to create the grid from the provided
        mission_key

        Args:
        key: str - the processed key ready for insertion
        valid: str - a required named parameter containing all valid symbols

        Returns:
            Grid_t - a 2d array built out of the provided key

        Raises:
        AssertionError - if the grid is the wrong dimensions
        """
        grid: Grid_t = []

        # Use a generator to populate the grid with the contents of the key
        key_generator = batched(key, 6)
        for gen_obj in key_generator:
            grid.append(list(gen_obj))

        # Fill the last row with valid elements
        valid.reverse()
        while len(grid[-1]) < 6:
            grid[-1].append(valid.pop())

        # Ensure the table is full by continually populating it
        valid.reverse()
        valid_char_generator = batched(valid, 6)
        grid.extend([list(x) for x in valid_char_generator if len(x)])

        assert len(grid) == 6, len(grid)
        assert len(grid[0]) == 6, len(grid[0])
        assert len(grid[-1]) == 6, len(grid[-1])
        return grid

    def get_grid(self) -> Grid_t:
        """ Return a copy of the grid"""

        return copy.deepcopy(self._grid)

    def prepare_message(self, message: str) -> str:
        """
        Convert a provided string into a message ensuring all chars are
        uppercase or digits

        Args:
        message: str - raw message provided by the caller

        Returns:
        str - the processed string message
        """
        # declare a variable here outside of the list for less allocations
        valid_insertions = string.ascii_uppercase + string.digits

        return "".join([
            c.upper()
            for c in message
            if c.upper() in valid_insertions
        ])

    def _find_position(self, *, left: str, right: str | None) -> Position_t:
        """
        Get the coordinates of two characters in the stored grid

        Args:
        left: str, right: str | None - two chars to look for in the grid

        Returns:
        Position_t - The locations of the two chars
        """
        ret: list[Coordinate | None] = [None, None]

        for idx, line in enumerate(self._grid):
            for idy, char in enumerate(line):
                if char == left:
                    ret[0] = Coordinate(idx, idy)
                elif char == right:
                    ret[1] = Coordinate(idx, idy)

        return tuple(ret)

    def _create_pairs(self, message: str) -> Iterator[tuple[str, ...]]:
        """
        A generator that yields a new pair of characters from the message
        on each call

        Args:
        message: str - the string to batch

        Yields:
        A tuple of at most two chars from the message
        """
        yield from batched(message, 2)

    def _handle_single(self, char: str, func: func_t) -> str:
        """
        Find the char at wrapped relative position -1, -1 to the provided
        char in the grid

        Args:
        char: str - a character in the grid
        func: func_t - a function to apply when moving around the grid

        Returns:
        str - the char to append to an encoded message
        """
        pos: Coordinate = self._find_position(left=char, right=None)[0]
        # Mod the coordinate to wrap around
        return self._grid[func(pos.x, 1) % 6][func(pos.y, 1) % 6]

    def _rectangle_rule(self, pair: Position_t) -> str:
        """
        Translating the characters at two given positions as per the rectangle
        rule

        Args:
        pair: Position_t - the positions of two chars in the grid

        Returns:
        str - the encoded string of two characters

        Raises
        AssertionError if either position provided is None
        """

        assert pair[0] is not None
        assert pair[1] is not None
        # Flip the co-ordinates around to find the opposite corners of the
        # given rectangle
        return (
            self._grid[pair[1].x][pair[0].y] +
            self._grid[pair[0].x][pair[1].y]
        )

    def _row_rule(self, pair: Position_t, func: func_t) -> str:
        """
        Shift both characters to the right, wrapping around, in the grid

        Args:
        pair: Position_t - the positions of two characters to find in the
        grid
        func: func_t - a function to apply when moving around the grid

        Returns:
        str - a two-character encoded string
        """
        ret = ""
        for loc in pair:
            if loc is None:
                continue

            ret += self._grid[loc.x][(func(loc.y, 1)) % 6]

        return ret

    def _col_rule(self, pair: Position_t, func: func_t) -> str:
        """
        Shift both characters down, wrapping around, in the grid

        Args:
        pair: Position_t - the positions of two characters to find in the grid
        func: func_t - a function to apply when moving around the grid

        Returns:
        str - a two-character encoded string
        """

        ret = ""
        for loc in pair:
            if loc is None:
                continue
            ret += self._grid[func(loc.x, 1) % 6][loc.y]
        return ret

    def encode_message(self, message: str) -> str:
        """
        Encode the message by parts

        Args:
        messsge: str - the messge to encode

        Returns:
        str - Encoded message
        """
        result = ""

        for pair in self._create_pairs(message.upper().replace(" ", "")):
            if len(pair) == 1:
                result += self._handle_single(pair[0], operator.sub)
                continue

            pos: Position_t = self._find_position(left=pair[0], right=pair[1])
            match pos[0].equal(pos[1]):
                case Equality.NOMATCH:
                    result += self._rectangle_rule(pos)
                case Equality.X_ONLY:
                    result += self._row_rule(pos, operator.add)
                case Equality.Y_ONLY:
                    result += self._col_rule(pos, operator.add)

        return result

    def decode_message(self, message: str) -> str:
        """
        Deocde the provided message

        Args:
        message: str - the message to decode

        Returns:
        str - the decoded message
        """
        result = ""

        for pair in self._create_pairs(message.upper().replace(" ", "")):
            if len(pair) == 1:
                result += self._handle_single(pair[0], operator.add)
                continue

            pos: Position_t = self._find_position(left=pair[0], right=pair[1])
            match pos[0].equal(pos[1]):
                case Equality.NOMATCH:
                    result += self._rectangle_rule(pos)
                case Equality.X_ONLY:
                    result += self._row_rule(pos, operator.sub)
                case Equality.Y_ONLY:
                    result += self._col_rule(pos, operator.sub)

        return result


if __name__ == "__main__":
    import unittest

    class TestSuite(unittest.TestCase):
        def test_Coordinate_equal(self):
            p1 = Coordinate(1, 1)
            p2 = Coordinate(1, 3)
            self.assertEqual(p1.equal(p2), Equality.X_ONLY)

            p3 = Coordinate(2, 3)
            self.assertEqual(p1.equal(p3), Equality.NOMATCH)
            self.assertEqual(p2.equal(p3), Equality.Y_ONLY)

        def test_batched(self):
            actual = batched("aboba", 2)
            expected = [("a", "b"), ("o", "b"), ("a",)]
            self.assertEqual(actual, expected)


        def test_CommunicationProtocol_constructor(self):
            c = CommunicationProtocol("MARS2025")
            expected = [
                ["M", "A", "R", "S", "2", "0"],
                ["5", "B", "C", "D", "E", "F"],
                ["G", "H", "I", "J", "K", "L"],
                ["N", "O", "P", "Q", "T", "U"],
                ["V", "W", "X", "Y", "Z", "1"],
                ["3", "4", "6", "7", "8", "9"]
            ]

            self.assertEqual(c._grid, expected)

        def test_CommunicationProtocol_create_grid(self):
            # Intentionally left out the second `2` as removing that is
            # handled elsewhere
            c = CommunicationProtocol("MARS205")
            valid = "BCDEFGHIJKLNOPQTUVWXYZ1346789"
            grid = c._create_grid(key="MARS205", valid=list(valid))
            expected = [
                ["M", "A", "R", "S", "2", "0"],
                ["5", "B", "C", "D", "E", "F"],
                ["G", "H", "I", "J", "K", "L"],
                ["N", "O", "P", "Q", "T", "U"],
                ["V", "W", "X", "Y", "Z", "1"],
                ["3", "4", "6", "7", "8", "9"]
            ]

            self.assertEqual(grid, expected)

        def test_CommunicationProtocol_prepare_message(self):
            c = CommunicationProtocol("MARS2025")
            self.assertEqual(c.prepare_message("foo!_2"), "FOO2")

        def test_CommunicationProtocol_find_position(self):
            c = CommunicationProtocol("MARS2025")
            pos = c._find_position(left="M", right="G")

            self.assertNotEqual(pos[0], None)
            self.assertNotEqual(pos[1], None)
            self.assertEqual(pos[0], Coordinate(0, 0))
            self.assertEqual(pos[1], Coordinate(2, 0))

        def test_CommunicationProtocol_create_pairs(self):
            c = CommunicationProtocol("MARS2025")
            gen = c._create_pairs("ABOBA")
            self.assertEqual(next(gen), ("A", "B"))
            self.assertEqual(next(gen), ("O", "B"))
            self.assertEqual(next(gen), ("A",))

        def test_CommunicationProtocol_handle_single(self):
            c = CommunicationProtocol("MARS2025")
            self.assertEqual(c._handle_single("A", operator.sub), "3")
            self.assertEqual(c._handle_single("N", operator.sub), "L")

        def test_CommunicationProtocol_rectangle_rule(self):
            c = CommunicationProtocol("MARS2025")
            input = Coordinate(4, 1), Coordinate(2, 3)
            self.assertEqual(c._rectangle_rule(input), "HY")
            input2 = Coordinate(0, 2), Coordinate(3, 1)
            self.assertEqual(c._rectangle_rule(input2), "PA")

        def test_CommunicationProtocol_row_rule(self):
            c = CommunicationProtocol("MARS2025")
            input = Coordinate(0, 2), Coordinate(0, 1)
            self.assertEqual(c._row_rule(input, operator.add), "SR")

        def test_CommunicationProtocol_col_rule(self):
            c = CommunicationProtocol("MARS2025")
            input = Coordinate(5, 0), Coordinate(1, 0)
            self.assertEqual(c._col_rule(input, operator.add), "MG")

        def test_CommunicationProtocol_encode_message(self):
            c = CommunicationProtocol("MARS2025")
            input = "Rover at 5N"
            expected = "PA5ZSRENL"
            self.assertEqual(c.encode_message(input), expected)

        def test_CommunicationProtocol_decode_message(self):
            c = CommunicationProtocol("MARS2025")
            self.assertEqual(c.decode_message("PA5ZSRENL"), "ROVERAT5N")

    unittest.main(verbosity=2)
