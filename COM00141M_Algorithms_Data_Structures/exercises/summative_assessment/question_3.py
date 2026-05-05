# Mars Rover Communication System
from __future__ import annotations

import copy
import itertools
import operator
import string
from enum import Enum
from typing import Callable
from typing import Iterator
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

