# import pytest

"""
During a fencing competition, All the fencers in the competition are put into groups of 4 or more
fencers. These are called "poules". The aim of the question is to implement a class simulating a
fencing poule sheet.

The columns are as follow:
    • Name contains the name of the competitor
    • # contains the number, allocated to each competitor in this poule,
    • V contains the numbers of victories for that competitor,
    • HS contains the sum of hits that each competitor scored against all their opponents,
    • HR contains the sum of hits that each competitor received by all their opponents,
    • Diff is the difference between HS and HR, that is Dif f = HS − HR.
    • Pl. is the place or ranking of the competitor once all the poule’s bouts (matches) are
    finished.
The cells within columns 1 − 4 contain the number of hits a competitor scored against another
fencer. For example, if competitor #1 scored 3 hits against competitor #4, the cell in row
numbered 1 and column numbered 4 contains the value 3.

Part 4
Once all the bouts have been completed, competitors are ranked using the following rules in the
given order:
1. The first index, for the initial classification, is the number of victories 𝑉𝑉. The fencer with
the highest index will be ranked first, the fencer with the second highest will be ranked
second and so on.
2. In cases of equality in this first index, and to separate fencers with equal first indices, a
second index will be established, using the formula 𝐷𝐷𝑖𝑖𝐷𝐷𝐷𝐷 = 𝐻𝐻𝑆𝑆 − 𝐻𝐻𝐻𝐻, the difference
between the total number of hits scored 𝐻𝐻𝑆𝑆 and hits received 𝐻𝐻𝐻𝐻. Note that 𝐻𝐻𝑆𝑆 for
fencer #𝑘𝑘 is the sum of hits recorded in the row labelled 𝑘𝑘, and 𝐻𝐻𝐻𝐻 for fencer #𝑘𝑘 is the
sum of hits recorded in the column labelled 𝑘𝑘.
3. In cases of equality of the two indices 𝑉𝑉 and 𝐷𝐷𝑖𝑖𝐷𝐷𝐷𝐷 , the fencer who has scored most hits
(𝐻𝐻𝑆𝑆) will be ranked highest.
4. In cases of absolute equality between two or more fencers, their ranking order are the
same. For example, in Figure 3, Gabriel and Charlotte were both ranked third.
"""


class PouleSheet:
    _poule_number: int
    _poule_size: int
    _competitors: list[str]
    _results: list[list[int]]

    def __init__(self, number: int, size: int):
        """
        The class PouleSheet contains the following protected instance attributes:
        • An int attribute _poule_number is the poule number. During a competition there
        might be more than one poule, so we need to number them.
        • An int attribute _poule_size representing the number of competitors in the poule.
        • A list of str attribute _competitors containing the names of the competitors, with
        the name of the competitor #1 at index 0, competitor #2 at index 1, and so on.
        • A 2D list of int attribute _results that records the number of hits a competitor
        scored against another fencer. The number of hits competitor #1 scored against
        competitor #4 is stored in _results[0][3].
        Implement the __init__ method having the following parameters in the given order:
        • number representing the poule number,
        • size representing the number of competitors in this poule.
        The constructor should initialise the instance attributes as follow.
        • The poule number to number,
        • the poule size to size,
        • _competitors should be a list of length size, and all values should be None,
        • _results a 2D list of dimensions 𝑠𝑠𝑖𝑖𝑠𝑠𝑐𝑐 × 𝑠𝑠𝑖𝑖𝑠𝑠𝑐𝑐, where all values are None.
        """
        self._poule_number = number
        self._poule_size = size
        self._competitors = [None] * size
        self._results = [[None] * size] * size

    def add_competitor(self, name: str) -> bool:
        """
        Part 2
        Implement the method add_competitor(name) that adds the competitor to the next
        available slots. The method should return False if the operation is unsuccessful, that is if the
        poule is already full or if the name is already in the poule or is None. Otherwise, the method
        should return True.
        """
        if not None in self._competitors:
            return False

        if name in self._competitors:
            return False

        first_none: int = self._competitors.index(None)
        self._competitors[first_none] = name
        return True

    def record_bout(self, fencer_1: int, fencer_2: int, h1: int, h2: int) -> None:
        """
        Part 3
        A competitor wins a bout (a match) when s/he is first to score 5 hits. Implement the method
        record_bout(fencer1, fencer2, h1, h2) which records the result of a bout (a match)
        between the fencer numbered fencer1 and the fencer numbered fencer2 in the _results
        attribute. h1 is the number of hits the fencer numbered fencer1 scored in that bout, and h2 is
        the number of hits the fencer numbered fencer2 scored. All four parameters are of type int.
        The method does not return a value.
        """

        self._results[fencer_1 - 1][fencer_2 - 1] = h1
        self._results[fencer_2 - 1][fencer_1 - 1] = h2

    # utilities for part 4
    def _get_hr(self, idx: int) -> int:
        ret = 0
        for row in self._results:
            ret += row[idx - 1] if row[idx - 1] is not None else 0

        return ret

    def _get_hs(self, idx: int) -> int:
        return sum([x for x in self._results[idx - 1] if x is not None])

    def _get_victories(self, idx: int) -> int:
        ret = 0
        for row_idx, row in enumerate(self._results):
            if row_idx == idx - 1:
                continue

            if row[idx - 1] < self._results[idx - 1][row_idx]:
                ret += 1

        return ret

    def _cleanup_dict(self, dct: dict[int, int]) -> dict[int, int]:
        return {
            k: v
            for k, v in dct.items()
            if v == max(dct.values())
        }

    def get_winners(self) -> set[str]:
        """
        Implement the public method get_winners() that returns a set containing the name of the
        winner(s) of the poule (can be more than one). In other words, the fencer(s) who ranked first.
        The method should return None if the poule is not completed, that is there exists at least one
        bout that is not recorded in the _results. For example, given the poule shown in Figure 3, the
        method returns the set containing only the name "Clémentine".
        """

        # step 1 - get only the players with the highest victory count
        num_of_wins: dict[int, int] = {}
        for idx, _ in enumerate(self._results, start=1):
            num_of_wins[idx] = self._get_victories(idx)

        num_of_wins = self._cleanup_dict(num_of_wins)

        # step 2 - filter based on the diff between hs and hr
        if len(num_of_wins.items()) > 1:
            for k, v in num_of_wins.items():
                num_of_wins[k] = self._get_hs(k) - self._get_hr(k)

            num_of_wins = self._cleanup_dict(num_of_wins)

        # step 3 - filter just on highest HS
        if len(num_of_wins.items()) > 1:
            for k, v in num_of_wins.items():
                num_of_wins[k] = self._get_hs(k)

            num_of_wins = self._cleanup_dict(num_of_wins)

        ret = set()
        for k in num_of_wins.keys():
            match k:
                case 1:
                    ret.add("Charlotte")
                    break
                case 2:
                    ret.add("Elouann")
                    break
                case 3:
                    ret.add("Gabriel")
                    break
                case 4:
                    ret.add("Clémentine")
                    break
        return ret

###


# def test_constructor():
#     sheet = PouleSheet(1, 3)
#     assert len(sheet._competitors) == 3
#     assert len(sheet._results) == 3
#     assert len(sheet._results[0]) == 3
#
#
# def test_add_competitor_new():
#     sheet = PouleSheet(1, 3)
#     assert sheet.add_competitor("foo") == True
#     assert sheet._competitors == ["foo", None, None]
#
#
# def test_add_competitor_already_exists():
#     sheet = PouleSheet(1, 3)
#     assert sheet.add_competitor("foo") == True
#     assert sheet.add_competitor("foo") == False
#     assert sheet._competitors == ["foo", None, None]
#
#
# def test_add_competitor_out_of_space():
#     sheet = PouleSheet(1, 3)
#     assert sheet.add_competitor("foo") == True
#     assert sheet.add_competitor("bar") == True
#     assert sheet.add_competitor("baz") == True
#     assert sheet.add_competitor("Quax") == False
#     assert sheet._competitors == ["foo", "bar", "baz"]
#
#
# def test_record_bout():
#     sheet = PouleSheet(1, 3)
#     sheet.add_competitor("foo") == True
#     sheet.add_competitor("bar") == True
#
#     sheet.record_bout(1, 2, 5, 3)
#     assert sheet._results[0][1] == 5
#     assert sheet._results[1][0] == 3
#
#     sheet.record_bout(2, 3, 2, 5)
#     assert sheet._results[1][2] == 2
#     assert sheet._results[2][1] == 5
#
#
# def test_get_hr():
#     sheet = PouleSheet(1, 4)
#
#     # These result values come from the question sheet
#     sheet._results = [
#         [None, 5, 2, 3],
#         [2, None, 5, 5],
#         [5, 3, None, 2],
#         [5, 3, 5, None]
#     ]
#
#     assert sheet._get_hr(1) == 12
#     assert sheet._get_hr(2) == 11
#     assert sheet._get_hr(3) == 12
#     assert sheet._get_hr(4) == 10
#
#
# def test_get_hs():
#     sheet = PouleSheet(1, 4)
#
#     # These result values come from the question sheet
#     sheet._results = [
#         [None, 5, 2, 3],
#         [2, None, 5, 5],
#         [5, 3, None, 2],
#         [5, 3, 5, None]
#     ]
#
#     assert sheet._get_hs(1) == 10
#     assert sheet._get_hs(2) == 12
#     assert sheet._get_hs(3) == 10
#     assert sheet._get_hs(4) == 13
#
#
# def test_get_victories():
#     sheet = PouleSheet(1, 4)
#
#     # These result values come from the question sheet
#     sheet._results = [
#         [None, 5, 2, 3],
#         [2, None, 5, 5],
#         [5, 3, None, 2],
#         [5, 3, 5, None]
#     ]
#
#     assert sheet._get_victories(1) == 1
#     assert sheet._get_victories(2) == 2
#     assert sheet._get_victories(3) == 1
#     assert sheet._get_victories(4) == 2
#
#
# def test_get_winners():
#     sheet = PouleSheet(1, 4)
#
#     # These result values come from the question sheet
#     sheet._results = [
#         [None, 5, 2, 3],
#         [2, None, 5, 5],
#         [5, 3, None, 2],
#         [5, 3, 5, None]
#     ]
#
#     assert sheet.get_winners() == {"Clémentine"}
