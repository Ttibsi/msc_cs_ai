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

    def __init__(self, mission_key: str) -> Self:
        """
        Construct a new CommunicationProtocol object

        Args:
        mission_key: str - Provide the initial mission key

        Return:
        Self - an object of type CommunicationProtocol
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
    
    def _create_grid(self, *, key: str, valid: str) -> Grid_t:
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
                if len(stripped_key) < curr_key:
                    grid[i][j] = stripped_key[curr_key]

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

    def _find_position(self, *, left: str, right: str) -> Position_t:
        """
        Get the coordinates of two characters in the stored grid

        Args:
        left: str, right: str - two chars to look for in the grid

        Returns:
        Position_t - The locations of the two chars 
        """
        ret: Position_t = None, None

        for idx, line in enumerate(self._grid):
            for idy, char in line:
                if char == left:
                    ret[0] = Coordinate(idx, idy)
                elif char == right:
                    ret[1] = Coordinate(idx, idy)

        return ret
        
    def _create_pairs(self, message:str) -> Iterator[tuple[str, ...]]:
        """
        A generator that yields a new pair of characters from the message 
        on each call

        Args:
        message: str - the string to batch 

        Yields:
        A tuple of at most two chars from the message
        """
        yield itertools.batched(message, 2)

    def _handle_single(self, char: str) -> str:
        """
        """
        pass

    def _rectangle_rule(self, pair:tuple[str,str]) -> str:
        """
        """
        pass

    def _row_rule(self, pair:tuple[str,str]) -> str:
        """
        """
        pass

    def _col_rule(self, pair:tuple[str,str]) -> str:
        """
        """
        pass

    def encode_message(self, message:str) -> str:
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
                    result += self._rectangle_rule(pair)
                case Equality.X_ONLY:
                    result += self._row_rule(pair)
                case Equality.Y_ONLY:
                    result += self._col_rule(pair)

        return ret



if __name__ == "__main__":
    import unittest

    class TestSuite(unittest.TestCase):
        def test_Coordinate_equal(self):
            pass

        def test_CommunicationProtocol_constructor(self):
            pass

        def test_CommunicationProtocol_create_message(self):
            pass

        def test_CommunicationProtocol_get_grid(self):
            pass

        def test_CommunicationProtocol_prepare_message(self):
            pass

        def test_CommunicationProtocol_find_position(self):
            pass

        def test_CommunicationProtocol_create_pairs(self):
            pass

        def test_CommunicationProtocol_encode_message(self):
            pass
