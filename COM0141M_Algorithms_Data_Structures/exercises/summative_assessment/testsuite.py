import operator
import unittest

import question_1 as q1
import question_2 as q2
import question_3 as q3

class TestQuestion1(unittest.TestCase):
    def test_construct_enrolment(self):
        """ unit test for the Enrollment constructor """
        input: enrolment_t = {}
        s_id = "2468"

        with self.assertRaises(ValueError, msg="Grade not found"):
            e = q1.Enrolment(input, s_id)

        input = {"grade": 12.3}
        err_msg = "Floating point grade fouund"
        with self.assertRaises(ValueError, msg=err_msg):
            e = q1.Enrolment(input, s_id)

        input["course_code"] = "C0012"
        input["grade"] = 32
        e = q1.Enrolment(input, s_id)

        self.assertEqual(e.grade, 32)
        self.assertEqual(e.course_code, "C0012")
        self.assertEqual(e.student_id, "2468")

    def test_compute_descriptive_stats(self):
        """ unit tests for the compute_descriptive_stats function """
        # Test with only a single item input
        input: list[int] = [1]
        expected: dict[str, float] = {
            "mean": 1.00,
            "median": 1.00,
            "std_dev": 0.00,
            "student_count": 1
        }

        self.assertEqual(q1.compute_descriptive_stats(input), expected)

        input = [56, 45, 76, 85]
        expected = {
            "mean": 65.50,
            "median": 66.00,
            "std_dev": 18.27,
            "student_count": 4
        }
        self.assertEqual(q1.compute_descriptive_stats(input), expected)

    def test_compute_course_statistics(self):
        """ unit test for the compute_course_statistics function """
        with self.assertRaises(ValueError, msg="Students dict is empty"):
            q1.compute_course_statistics({})

        students = {
            "S001": {
                "name": "Alice",
                "enrolments": [
                    {"course_code": "CS5001", "grade": 72},
                    {"course_code": "CS5002", "grade": 65}
                ]
            }
        }

        expected = {
            "CS5001": {"mean": 72.00, "median": 72.00, "std_dev": 0.00, "student_count": 1},
            "CS5002": {"mean": 65.00, "median": 65.00, "std_dev": 0.00, "student_count": 1}
        }
        actual = q1.compute_course_statistics(students)
        self.assertEqual(actual, expected)

    def test_format_course_report(self):
        """ unit test for the format_course_report function """
        input = {
            "CS5001": {"mean": 72.00, "median": 72.00, "std_dev": 0.00, "student_count": 1},
            "CS5002": {"mean": 65.00, "median": 65.00, "std_dev": 0.00, "student_count": 1}
        }

        expected = """\
Course Mean Median StdDev Students
-----------------------------------
CS5001 72.00 72.00 0.00 1
CS5002 65.00 65.00 0.00 1\
"""

        self.assertEqual(q1.format_course_report(input), expected)

class TestQuestion2(unittest.TestCase):
    def test_Find_distance(self):
        f = q2.Find(5, 2)
        g = q2.Find(9, 9)
        self.assertEqual(f.distance(g), 8.06)

    def test_Site_add(self):
        s = q2.Site(5, 5, [])
        s.add(q2.Find(1, 2))
        self.assertEqual(len(s.discoveries), 1)

    def test_Site_validate(self):
        s = q2.Site(5, 5, [])

        with self.assertRaises(ValueError):
            s.validate(0, 2)

        with self.assertRaises(ValueError):
            s.validate(4, 12)

        # We need to check if this doesn't throw an error
        self.assertEqual(s.validate(2, 2), None)

    def test_Distance_lt(self):
        f1 = q2.Find(1, 1)
        f2 = q2.Find(4, 4)
        f3 = q2.Find(2, 2)
        d = q2.Distance(f1, f2, f1.distance(f2))
        e = q2.Distance(f1, f3, f1.distance(f3))

        self.assertEqual(e < d, True)
        self.assertEqual(d < e, False)

    def test_new_site(self):
        expected = q2.Site(5, 5, [])
        self.assertEqual(q2.new_site(5, 5), expected)

    def test_add_find(self):
        s = q2.Site(5, 5, [])
        expected = q2.Site(5, 5, [q2.Find(1, 1)])
        self.assertEqual(q2.add_find(s, 1, 1), expected)

        with self.assertRaises(ValueError):
            q2.add_find(s, 6, 6)

    def test_distance(self):
        f = q2.Find(5, 2)
        g = q2.Find(9, 9)
        self.assertEqual(q2.distance(f, g), 8.06)

    def test_get_helper(self):
        lst = [1, 2, 3]
        self.assertEqual(q2._get(lst, 7), None)
        self.assertEqual(q2._get(lst, 1), 2)

    def test_closest_artefacts(self):
        s = q2.Site(10, 10, [q2.Find(1, 4), q2.Find(3, 1), q2.Find(6, 7), q2.Find(9, 5)])
        expected = q2.Distance(q2.Find(1, 4), q2.Find(3, 1), 3.61)
        self.assertEqual(q2.closest_artefacts(s), expected)

    def test_in_circle(self):
        s = q2.Site(10, 10, [q2.Find(1, 1), q2.Find(5, 5), q2.Find(8, 8)])
        self.assertEqual(q2.in_circle(s, 5, 5, 3), [q2.Find(5, 5)])

        s2 = q2.Site(10, 10, [q2.Find(3, 4), q2.Find(7, 7), q2.Find(3, 4), q2.Find(9, 9)])
        self.assertEqual(
            q2.in_circle(s2, 0, 0, 5.1),
            [q2.Find(3, 4), q2.Find(3, 4)]
        )

class TestSuite(unittest.TestCase):
    def test_Coordinate_equal(self):
        p1 = q3.Coordinate(1, 1)
        p2 = q3.Coordinate(1, 3)
        self.assertEqual(p1.equal(p2), q3.Equality.X_ONLY)

        p3 = q3.Coordinate(2, 3)
        self.assertEqual(p1.equal(p3), q3.Equality.NOMATCH)
        self.assertEqual(p2.equal(p3), q3.Equality.Y_ONLY)

    def test_batched(self):
        actual = q3.batched("aboba", 2)
        expected = [("a", "b"), ("o", "b"), ("a",)]
        self.assertEqual(actual, expected)

    def test_CommunicationProtocol_constructor(self):
        c = q3.CommunicationProtocol("MARS2025")
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
        c = q3.CommunicationProtocol("MARS205")
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
        c = q3.CommunicationProtocol("MARS2025")
        self.assertEqual(c.prepare_message("foo!_2"), "FOO2")

    def test_CommunicationProtocol_find_position(self):
        c = q3.CommunicationProtocol("MARS2025")
        pos = c._find_position(left="M", right="G")

        self.assertNotEqual(pos[0], None)
        self.assertNotEqual(pos[1], None)
        self.assertEqual(pos[0], q3.Coordinate(0, 0))
        self.assertEqual(pos[1], q3.Coordinate(2, 0))

    def test_CommunicationProtocol_create_pairs(self):
        c = q3.CommunicationProtocol("MARS2025")
        gen = c._create_pairs("ABOBA")
        self.assertEqual(next(gen), ("A", "B"))
        self.assertEqual(next(gen), ("O", "B"))
        self.assertEqual(next(gen), ("A",))

    def test_CommunicationProtocol_handle_single(self):
        c = q3.CommunicationProtocol("MARS2025")
        self.assertEqual(c._handle_single("A", operator.sub), "3")
        self.assertEqual(c._handle_single("N", operator.sub), "L")

    def test_CommunicationProtocol_rectangle_rule(self):
        c = q3.CommunicationProtocol("MARS2025")
        input = q3.Coordinate(4, 1), q3.Coordinate(2, 3)
        self.assertEqual(c._rectangle_rule(input), "HY")
        input2 = q3.Coordinate(0, 2), q3.Coordinate(3, 1)
        self.assertEqual(c._rectangle_rule(input2), "PA")

    def test_CommunicationProtocol_row_rule(self):
        c = q3.CommunicationProtocol("MARS2025")
        input = q3.Coordinate(0, 2), q3.Coordinate(0, 1)
        self.assertEqual(c._row_rule(input, operator.add), "SR")

    def test_CommunicationProtocol_col_rule(self):
        c = q3.CommunicationProtocol("MARS2025")
        input = q3.Coordinate(5, 0), q3.Coordinate(1, 0)
        self.assertEqual(c._col_rule(input, operator.add), "MG")

    def test_CommunicationProtocol_encode_message(self):
        c = q3.CommunicationProtocol("MARS2025")
        input = "Rover at 5N"
        expected = "PA5ZSRENL"
        self.assertEqual(c.encode_message(input), expected)

    def test_CommunicationProtocol_decode_message(self):
        c = q3.CommunicationProtocol("MARS2025")
        self.assertEqual(c.decode_message("PA5ZSRENL"), "ROVERAT5N")

unittest.main(verbosity=2)
