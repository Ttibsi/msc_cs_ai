# University Analytics System
import collections
from dataclasses import dataclass
import statistics
from typing import Any

type enrolment_t = dict[str, str | int | float]

class Enrolment:
    grade: int
    course_code: str
    name: str
    student_id: str

    def __init__(self, data: dict[str, Any], name: str, s_id: str):
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

        self.course_code = data.get("course_code", None)
        if self.course_code is None:
            raise ValueError("Course Code not found")

        self.name = name
        self.studen_id = s_id


@dataclass
class Course:
    grades: list[int]
    student_ids: set[str]


def compute_descriptive_stats(grades: list[int]) -> dict[str, float]:
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
        "std_dev": float(stdev)
        "student_count": float(f"{len(grades):.2f}")
    }

def compute_course_statistics(students) -> dict[str, dict[str, int]]:
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
            raise ValueError("enrollment data not provided")

        for course_data in enrollments:
            structured_enrolments.append(
                Enrolment(course_data, name, student_id)
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
