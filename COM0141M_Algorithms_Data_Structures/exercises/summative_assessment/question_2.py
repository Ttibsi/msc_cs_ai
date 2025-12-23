# Archaeological dig site artefact recoding
import math
from typing import Any
from typing import NamedTuple
from typing import Self

# Create a named tuple for any Find to ensure the data is more structured
class Find(NamedTuple):
    x: int
    y: int

    def distance(self, other: Self | None) -> float:
        """
        Calculate the euclidian distance between two different Find objects
        """

        if other is None:
            return 10000000.0  # arbitrarily large number
        x_half = (other.x - self.x) * 2
        y_half = (other.y - self.y) * 2
        return round(math.sqrt(x_half + y_half), 2)


class Site(NamedTuple):
    max_x: int
    max_y: int
    discoveries: list[Find]

    def add(self, find: Find) -> None:
        """ Add a new Find to the discoveries """
        self.discoveries.append(find)

    def validate(self, x: int, y: int) -> None:
        """
        Raise a ValueError if the coordinates for a potential find aren't valid
        """

        if x == 0 or y == 0:
            raise ValueError("Coordinates cannot be 0")

        if x > self.max_x or y > self.max_y:
            raise ValueError("Coordinates cannot exceed max coordinates")


class Distance(NamedTuple):
    p: Find
    q: Find
    distance: float

    def __lt__(self, other: Self) -> bool:
        """
        Operator overload to compare two objects on their `distance` attribute
        """
        if not isinstance(other, Distance):
            raise ValueError("Incorrect type provided")
        return self.distance < other.distance


def new_site(max_x: int, max_y: int) -> Site:
    """
    Create a new dig site, a c-style constructor

    Args:
        max_x: int - the largest x coordinate for the site
        max_y: int - the largest y coordinate for the site

    Returns:
        Site - a new Site object

    Raises:
        ValueError if max_x or max_y are less than 0
    """

    if max_x <= 0 or max_y <= 0:
        raise ValueError(f"Invalid value passed: x: {max_x}, y: {max_y}")
    return Site(max_x, max_y, [])


def add_find(site: Site, x: int, y: int) -> Site:
    """
    Add a new find to the site

    Args:
        site: Site - a valid Site object
        x: int - the x coordinate of the find
        y: int - the y coordinate of the find

    Returns:
        Site - the updated site object

    Raises:
        ValueError - if the provided coordinates are invalid
    """
    site.validate(x, y)
    site.add(Find(x, y))
    return site


def distance(p: Find | tuple[int, int], q: Find | tuple[int | int]) -> float:
    """
    Return the euclidian distance between two Finds

    Args:
        p: Find | tuple[int, int] - the coordinates of a found object
        q: Find | tuple[int, int] - the coordinates of a different found
                                    object

    Returns:
        float - the euclidian distance between those two objects
    """
    if isinstance(p, tuple):
        p = Find(*p)
    if isinstance(q, tuple):
        q = Find(*q)

    return p.distance(q)


def _get(lst: list[Any], idx: int) -> Any | None:
    """
    Helper function to find the element in a list with bounds checking

    Args:
        lst: list[Any] - any list object
        idx: int - the index to retrieve from

    Returns:
        Any - the element from the list
        None - if the index is out of bounds
    """
    if len(lst) < idx:
        return None
    return lst[idx]


def closest_artefacts(site: Site) -> Distance | None:
    """
    Recursive function to find the two closest artefacts at a given site

    Args:
        site: Site - a location to check

    Returns:
        Distance - the distance object that
    """

    def _closest_recursive(discoveries: list[Find]) -> Distance:
        """ Locally scoped recursive helper function. """
        # brute force - return the closest pair
        if len(discoveries) <= 3:
            # get the three discoveries
            disco_x = _get(discoveries, 0)
            disco_y = _get(discoveries, 1)
            disco_z = _get(discoveries, 2)

            xy_dist = disco_x.distance(disco_y)
            xz_dist = disco_x.distance(disco_z)
            yz_dist = disco_y.distance(disco_z)
            min_dist = min(xy_dist, xz_dist, yz_dist)

            if min_dist == xy_dist:
                return Distance(disco_x, disco_y, xy_dist)
            elif min_dist == yz_dist:
                return Distance(disco_y, disco_z, yz_dist)
            elif min_dist == xz_dist:
                return Distance(disco_x, disco_z, xz_dist)

        # otherwise, split the slice in half and recurse on both
        half = len(discoveries) // 2
        lhs = _closest_recursive(discoveries[0:half])
        rhs = _closest_recursive(discoveries[half:])
        straddle_dist = Distance(
            discoveries[half],
            discoveries[half + 1],
            discoveries[half].distance(discoveries[half + 1])
        )

        # pick the smaller pair:
        return min(lhs, rhs, straddle_dist)

    ### End of inner helper function

    if len(discoveries) < 2:
        return None

    return _closest_recursive(site.discoveries);


def in_circle(site: Site, cx: int, cy: int, r: int) -> list[Find]:
    """
    Find all discoveries within a given radius in a site

    Args:
        site: Site - the site to search
        cx: int, cy: int - the x and y coordinates of the centerpoint of
                           the circle
        r: int - the radius of the circle

    Returns:
        list[Find] - a list of all valid artifacts found in the circle
    """

    valid_finds: list[Find] = []
    return valid_finds


if __name__ == "__main__":
    # If this file is the main module run with `python3 question_2.py`,
    # execute the unit tests
    import unittest

    class TestSuite(unittest.TestCase):
        ...

    unittest.main(verbosity=2)
