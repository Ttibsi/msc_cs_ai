# Archaeological dig site artefact recoding
import math
from typing import Any
from typing import NamedTuple
from typing import Self


class Find(NamedTuple):
    """
    Create a named tuple for any Find to ensure the data is more structured
    """
    x: int
    y: int

    def distance(self, other: Self | None) -> float:
        """
        Calculate the euclidian distance between two different Find objects
        """

        if other is None:
            return 10000000.0  # arbitrarily large number
        x_half = math.pow(other.x - self.x, 2)
        y_half = math.pow(other.y - self.y, 2)
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
    try:
        return lst[idx]
    except IndexError:
        return None


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

            # We need to check if each value is None. If not, we
            # instead populate the value with an arbitrarily large
            # number
            xy_dist = disco_x.distance(disco_y) if disco_x is not None else 100
            xz_dist = disco_x.distance(disco_z) if disco_x is not None else 100
            yz_dist = disco_y.distance(disco_z) if disco_y is not None else 100
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

    # End of inner helper function

    if len(site.discoveries) < 2:
        return None

    return _closest_recursive(site.discoveries)


def in_circle(site: Site, cx: int, cy: int, r: float) -> list[Find]:
    """
    Find all discoveries within a given radius in a site

    Args:
        site: Site - the site to search
        cx: int, cy: int - the x and y coordinates of the centerpoint of
                           the circle
        r: float - the radius of the circle

    Returns:
        list[Find] - a list of all valid artifacts found in the circle
    """

    def _check_coordinates(x: int, y: int, cx: int, cy: int, r: float) -> bool:
        """
        Check the coordinates of a given Find lie within the provided circle
        dimensions using the formula:
        (x-center_x)^2 + (y - center_y)^2 < radius^2

        Args:
            x: int - x coordinate of the find
            y: int - y coordinate of the find
            cx: int - x coordinate of the center of the circle
            cy: int - y coordinate of the center of the circle
            r: float - radius of the circle

        Returns:
            bool - does the coordinates lie within the circle
        """
        return math.pow(x - cx, 2) + math.pow(y - cy, 2) <= math.pow(r, 2)

    valid_finds: list[Find] = []
    for find in site.discoveries:
        if _check_coordinates(find.x, find.y, cx, cy, r):
            valid_finds.append(find)

    return valid_finds


if __name__ == "__main__":
    # If this file is the main module run with `python3 question_2.py`,
    # execute the unit tests
    import unittest

    class TestSuite(unittest.TestCase):
        def test_Find_distance(self):
            f = Find(5, 2)
            g = Find(9, 9)
            self.assertEqual(f.distance(g), 8.06)

        def test_Site_add(self):
            s = Site(5, 5, [])
            s.add(Find(1, 2))
            self.assertEqual(len(s.discoveries), 1)

        def test_Site_validate(self):
            s = Site(5, 5, [])

            with self.assertRaises(ValueError):
                s.validate(0, 2)

            with self.assertRaises(ValueError):
                s.validate(4, 12)

            # We need to check if this doesn't throw an error
            self.assertEqual(s.validate(2, 2), None)

        def test_Distance_lt(self):
            f1 = Find(1, 1)
            f2 = Find(4, 4)
            f3 = Find(2, 2)
            d = Distance(f1, f2, f1.distance(f2))
            e = Distance(f1, f3, f1.distance(f3))

            self.assertEqual(e < d, True)
            self.assertEqual(d < e, False)

        def test_new_site(self):
            expected = Site(5, 5, [])
            self.assertEqual(new_site(5, 5), expected)

        def test_add_find(self):
            s = Site(5, 5, [])
            expected = Site(5, 5, [Find(1, 1)])
            self.assertEqual(add_find(s, 1, 1), expected)

            with self.assertRaises(ValueError):
                add_find(s, 6, 6)

        def test_distance(self):
            f = Find(5, 2)
            g = Find(9, 9)
            self.assertEqual(distance(f, g), 8.06)

        def test_get_helper(self):
            lst = [1, 2, 3]
            self.assertEqual(_get(lst, 7), None)
            self.assertEqual(_get(lst, 1), 2)

        def test_closest_artefacts(self):
            s = Site(10, 10, [Find(1, 4), Find(3, 1), Find(6, 7), Find(9, 5)])
            expected = Distance(Find(1, 4), Find(3, 1), 3.61)
            self.assertEqual(closest_artefacts(s), expected)

        def test_in_circle(self):
            s = Site(10, 10, [Find(1, 1), Find(5, 5), Find(8, 8)])
            self.assertEqual(in_circle(s, 5, 5, 3), [Find(5, 5)])

            s2 = Site(10, 10, [Find(3, 4), Find(7, 7), Find(3, 4), Find(9, 9)])
            self.assertEqual(
                in_circle(s2, 0, 0, 5.1),
                [Find(3, 4), Find(3, 4)]
            )

    unittest.main(verbosity=2)
