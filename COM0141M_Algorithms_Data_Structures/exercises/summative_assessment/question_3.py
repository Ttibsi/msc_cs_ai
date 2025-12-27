# Mars Rover Communication System
import copy
from enum import Enum
import string
import itertools
from typing import Iterator
from typing import NamedTuple
from typing import Self

# Set up helpers


class Equality(Enum):
    NOMATCH = 1
    X_ONLY = 2
    Y_ONLY = 3


class Coordinate(NamedTuple):
    x: int
    y: int

    def equal(self, other: Self) -> Equality:
        """ Compare two coordinate objects """
        if self.x == other.x:
            return Equality.X_ONLY
        if self.y == other.y:
            return Equality.Y_ONLY

        return Equality.NOMATCH


# Set up type aliases for clarity
type Position_t = tuple[Coordinate | None, Coordinate | None]
type Grid_t = list[list[str | None]]


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
        valid_insertions.reverse()
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
        """
        grid: Grid_t = [[None] * 6] * 6
        for i in range(6):
            for j in range(6):
                curr_key = (i * 6) + j
                if curr_key < len(key):
                    grid[i][j] = key[curr_key]

                else:
                    grid[i][j] = valid.pop()

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
        ret: Position_t = None, None

        for idx, line in enumerate(self._grid):
            for idy, char in enumerate(line):
                if char == left:
                    ret[0] = Coordinate(idx, idy)
                elif char == right:
                    ret[1] = Coordinate(idx, idy)

        return ret

    def _create_pairs(self, message: str) -> Iterator[tuple[str, ...]]:
        """
        A generator that yields a new pair of characters from the message
        on each call

        Args:
        message: str - the string to batch

        Yields:
        A tuple of at most two chars from the message
        """
        yield from itertools.batched(message, 2)

    def _handle_single(self, char: str) -> str:
        """
        Find the char at wrapped relative position -1, -1 to the provided
        char in the grid

        Args:
        char: str - a character in the grid

        Returns:
        str - the char to append to an encoded message
        """
        pos: Coordinate = self._find_position(char, None)[0]
        # Mod the coordinate to wrap around
        return self._grid[(pos.x - 1) % 6][(pos.y - 1) % 6]

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

        # Get the co-ordinates of the rectangle to draw in the grid
        top_row = min(pair[0].x, pair[1].x)
        left_col = min(pair[0].y, pair[1].y)
        bottom_row = max(pair[0].x, pair[1].x)
        right_col = max(pair[0].y, pair[1].y)
        length = bottom_row - top_row

        # construct a mini-grid out of the grid
        mini_grid = []
        for i in range(left_col, right_col + 1):
            row = []
            for j in range(top_row, bottom_row + 1):
                row.append(self._grid[i][j])

            mini_grid.append(row)

        # Build up the return string
        ret: str = ""

        for loc in pair:
            if loc is None:
                continue
            # NOTE: I think this logic is incorrect
            ret += mini_grid[loc.x % length][loc.y % length]

        return ret

    def _row_rule(self, pair: Position_t) -> str:
        """
        Shift both characters to the right, wrapping around, in the grid

        Args:
        pair: Position_t - the positions of two characters to find in the
        grid

        Returns:
        str - a two-character encoded string
        """
        ret = ""
        for loc in pair:
            if loc is None:
                continue

            ret += self._grid[loc.x][(loc.y + 1) % 6]

        return ret

    def _col_rule(self, pair: Position_t) -> str:
        """
        Shift both characters down, wrapping around, in the grid

        Args:
        pair: Position_t - the positions of two characters to find in the grid

        Returns:
        str - a two-character encoded string
        """

        ret = ""
        for loc in pair:
            if loc is None:
                continue
            ret += self._grid[(loc.x + 1) % 6][loc.y]
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

        for pair in self._create_pairs(message):
            if len(pair) == 1:
                result += self.handle_single(pair[0])

            pos: Position_t = self._find_position(left=pair[0], right=pair[1])
            match pos[0].equal(pos[1]):
                case Equality.NOMATCH:
                    result += self._rectangle_rule(pos)
                case Equality.X_ONLY:
                    result += self._row_rule(pos)
                case Equality.Y_ONLY:
                    result += self._col_rule(pos)

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
            c = CommunicationProtocol("MARS2025")
            valid = "BCDEFGHIJKLNOPQTUVWXYZ1346789"
            grid = c._create_grid(key="MARS2025", valid=list(valid))
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
            pass
        def test_CommunicationProtocol_rectangle_rule(self):
            pass
        def test_CommunicationProtocol_row_rule(self):
            pass
        def test_CommunicationProtocol_col_rule(self):
            pass
        def test_CommunicationProtocol_encode_message(self):
            pass

    unittest.main(verbosity = 2)
