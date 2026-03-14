import datetime
from enum import Enum
from typing import NamedTuple

class Title(Enum):
    MR = 0,
    MS = 1,
    MRS = 2, 
    DR = 3,


class Person(NamedTuple):
    title: Title | None
    surname: str
    given_names: str
    id_: str
    email: str
    company: str
    updated: datetime.date

    def __repr__(self) -> str:
        return f"{str(self.updated)} {self.given_names} {self.surname}"

def get_title_enum(titleStr: str) -> Title | None:
    if not titleStr:
        return None
    if "mrs" in titleStr.lower():
        return Title.MRS
    elif "dr" in titleStr.lower():
        return Title.DR
    elif "mr" in titleStr.lower():
        return Title.MR
    else: 
        return Title.MS

def date_to_obj(dateStr: str) -> datetime.date:
    return datetime.datetime.strptime(dateStr, "%d/%m/%Y").date()

def sort_data(data: list[Person]) -> None:
    data.sort(key=lambda x: x.updated)

def main() -> int:
    with open("PeopleTrainingDate.csv", "r") as f:
        lines = f.readlines()

    lines = lines[1:-1] # strip out headers and final newline
    data: list[Person] = []
    for line in lines:
        elems = line.strip().split(",")
        given_title = get_title_enum(elems[0])

        data.append(Person(
            given_title,
            elems[1][1:],  # strip the opening quote
            elems[2][1:-1], # strip the closing quote and opening space
            *elems[3:-1],
            date_to_obj(elems[-1])
        ))

    sort_data(data)
    print(data[0])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
