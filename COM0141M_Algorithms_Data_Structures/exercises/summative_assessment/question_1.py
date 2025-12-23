# University Analytics System

import collections
import statistics
from typing import Any

# Define useful type aliases for clarity in data structure
type enrolment_t = dict[str, str | int | float]
type students_t = dict[str, dict[str, str | list[enrolment_t]]]
type stats_t = dict[str, dict[str, int]]


class Enrolment:
    grade: int
    course_code: str
    student_id: str

    def __init__(self, data: enrolment_t, s_id: str):
        """
        Construct an object of the type Enrolment

        Parameters:
            - data: enrolment_t - a dictionary with two keys:
                                  `grade`, `course_code`
            - s_id: str - A string representation of the student's ID

        Raises:
            ValueError - incorrect data passed in the `data` dict
        """

        grade_val = data.get("grade", None)
        if grade_val is None:
            raise ValueError("Grade not found")
        elif isinstance(grade_val, float):
            raise ValueError("Floating point grade found")
        elif not (0 <= grade_val <= 100):
            # ensure the grade is between 0 and 100, inclusive
            raise ValueError("Invalid grade")
        else:
            self.grade = grade_val

        raw_course_code = data.get("course_code", None)
        if raw_course_code is None:
            raise ValueError("Course Code not found")
        self.course_code = raw_course_code

        self.student_id = s_id


# define Course type to better structure data during transformation
class Course:
    grades: list[int]
    student_ids: set[str]

    def __init__(self):
        """ Construct the Course object with default values """
        self.grades = []
        self.student_ids = set()


def compute_descriptive_stats(grades: list[int]) -> dict[str, float | int]:
    """
    Helper function to generate a dict of statistics based on a set of grades

    Args:
        - grades: list[int] - a list of student grades

    Returns:
        dict[str, float | int] - A dictionary of statistics calculated from
                                 the given grade set

    Raises:
        ValueError - Grades list doesn't provide valid data
    """

    if not grades:
        raise ValueError("Grades list is empty")
    if not all(str(g).strip('-').isdigit() for g in grades):
        raise ValueError("Invalid grade found")

    # if there's only a single value, the stdev is just 0
    # as the stdev is the average distance to the mean, and a length of 1
    # means the value itself is the mean of the data set
    stdev = f"{statistics.stdev(grades):.2f}" if len(grades) >= 2 else "0.00"

    return {
        "mean": float(f"{statistics.mean(grades):.2f}"),
        "median": float(f"{statistics.median(grades):.2f}"),
        "std_dev": float(stdev),
        "student_count": len(grades)
    }


def compute_course_statistics(students: students_t) -> stats_t:
    """
    Calculate statistics on multiple uni courses based on given student data

    Args:
        students: students_t - A dictionary containing each student and the
                               courses they're enrolled in

    Returns:
        stats_t - A dict containing statistics on courses attended by the
                  given students

    Raises:
        ValueError - provided dict is empty or otherwise contains invalid data
    """

    if not students:
        raise ValueError("Students dict is empty")

    # Extract the enrolment data into a more structured form
    structured_enrolments: list[Enrolment] = []
    for student_id, data in students.items():
        name: str | None = data.get("name", None)
        if name is None:
            raise ValueError("Name not provided")

        enrolments: list[enrolment_t] | None = data.get("enrolments", None)
        if enrolments is None:
            raise ValueError("enrolment data not provided")

        for course_data in enrolments:
            structured_enrolments.append(
                Enrolment(course_data, student_id)
            )

    # Extract enrolment data into course-specific data
    course_stats: dict[str, Course] = collections.defaultdict(Course)
    for enrolment in structured_enrolments:
        course_stats[enrolment.course_code].grades.append(enrolment.grade)
        course_stats[enrolment.course_code].student_ids.add(
            enrolment.student_id
        )

    # Collect all course data into one dict
    course_values: dict[str, dict[str, int]] = {}
    for code, course in course_stats.items():
        course_values[code] = compute_descriptive_stats(course.grades)

    return course_values


def format_course_report(course_stats: dict[str, dict[str, int]]) -> str:
    """
    Format the statistic data into a readable table

    Args:
    - course_stats: dict[str, dict[str | int]] - A dict of calculated stats
                                                 on course grades

    Returns:
        str - The formatted table as a single string
    """

    report_contents = [["Course", "Mean", "Median", "StdDev", "Students"]]

    # Add header line
    # Sum the length of all the text in the header, then add one for every
    # entry to ensure spaces
    header_line_len = sum([len(i) + 1 for i in report_contents[0]])
    report_contents.append(["-" * header_line_len])

    # Build up rows of data
    for course_code, stats in course_stats.items():
        # Ensure we collect all the data with default placeholder values
        report_contents.append([
            course_code,
            f"{stats.get("mean", 0.00):.2f}",
            f"{stats.get("median", 0.00):.2f}",
            f"{stats.get("std_dev", 0.00):.2f}",
            str(stats.get("student_count", 0))
        ])

    # Join our 2d array together into a single string
    intermediary = []
    for row in report_contents:
        intermediary.append(" ".join(str(elem) for elem in row))

    return "\n".join(intermediary)


if __name__ == "__main__":
    # if this file is the main module, run the unit tests
    import unittest

    class TestSuite(unittest.TestCase):
        def test_construct_enrolment(self):
            input: enrolment_t = {}
            s_id = "2468"

            with self.assertRaises(ValueError, msg="Grade not found"):
                e = Enrolment(input, s_id)

            input = {"grade": 12.3}
            err_msg = "Floating point grade fouund"
            with self.assertRaises(ValueError, msg=err_msg):
                e = Enrolment(input, s_id)

            input["course_code"] = "C0012"
            input["grade"] = 32
            e = Enrolment(input, s_id)

            self.assertEqual(e.grade, 32)
            self.assertEqual(e.course_code, "C0012")
            self.assertEqual(e.student_id, "2468")

        def test_compute_descriptive_stats(self):
            # Test with only a single item input
            input: list[int] = [1]
            expected: dict[str, float] = {
                "mean": 1.00,
                "median": 1.00,
                "std_dev": 0.00,
                "student_count": 1
            }

            self.assertEqual(compute_descriptive_stats(input), expected)

            input = [56, 45, 76, 85]
            expected = {
                "mean": 65.50,
                "median": 66.00,
                "std_dev": 18.27,
                "student_count": 4
            }
            self.assertEqual(compute_descriptive_stats(input), expected)

        def test_compute_course_statistics(self):
            with self.assertRaises(ValueError, msg="Students dict is empty"):
                compute_course_statistics({})

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
            actual = compute_course_statistics(students)
            self.assertEqual(actual, expected)

        def test_format_course_report(self):
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

            self.assertEqual(format_course_report(input), expected)

    unittest.main(verbosity=2)
