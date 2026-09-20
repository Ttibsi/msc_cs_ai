import argparse
import calendar
import csv
from collections import Counter
from collections.abc import Sequence
from typing import NamedTuple

class CSV(NamedTuple):
    headers: list[str]
    body: list[dict[str, str]]

def parse_csv(filename: str) -> CSV:
    headers = open(filename).readlines()[0].strip().split(",")
    body = []

    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            body.append(row)
            if body[-1]["children"] == "NA":
                body[-1]["children"] = "0"

    return CSV(headers, body)


def top_six_months(reservations: list[dict[str, str]]):
    cancellations_by_month: dict[str, int] = Counter()
    month_names = list(calendar.month_name)
    for row in reservations:
        if row["is_canceled"] == "1":
            month = month_names[int(row["reservation_status_date"].split("-")[1])]
            cancellations_by_month[month] += 1

    print("Top six months by cancellation")
    print("------------------------------")
    for month, count in cancellations_by_month.most_common(6):
        print(f"{month:>9}: {count}")
    print("")


def key_attributes(reservations: list[dict[str, str]]):
    print("Key Cancellation Predictors")
    print("---------------------------")
    # print("previous_cancellations + previous_bookings_not_canceled")
    # print("market_segment && distribution_channel ( Corporate )")

    previously_cancelled: int = 0
    not_previously_cancelled: int = 0
    modified: int = 0
    not_modified: int = 0
    customer_type: dict[str, int] = Counter()

    for row in reservations:
        if row["is_canceled"] == "1":
            if row["previous_cancellations"] == "0":
                not_previously_cancelled += 1
            else: 
                previously_cancelled += 1

            if row["booking_changes"] == "0":
                not_modified += 1
            else:
                modified += 1

            customer_type[row["customer_type"]] += 1

    print(f"Has previously cancelled? Yes {previously_cancelled}, No: {not_previously_cancelled}")
    print(f"Modified booking: Yes: {modified}, No: {not_modified}")
    print("Cancelled customer types by count:")
    for k, v in customer_type.items():
        print(f"{k:>16}: {v}")
    print()


def lead_time(reservations: list[dict[str, str]]):
    lead_time_count: dict[int, int] = Counter()
    for row in reservations:
        if row["is_canceled"] == "1":
            lt = int(row["lead_time"])
            lead_time_count[lt] += 1

    print("Top 15 Lead Times on cancelled reservations")
    print("-------------------------------------------")
    for x, y in lead_time_count.most_common(15):
        print(f"lead time: {x:03}, count: {y}")


# Only used if needed to print cancelled bookings in it's own CSV
def get_cancelled_only(reservations: CSV):
    with open('cancelled.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=reservations.headers)
        writer.writeheader()
        for row in reservations.body:
           if row["is_canceled"] == "1":
               writer.writerow(row)

    print("cancelled.csv generated")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cancelled", "-c", action="store_true")
    args = parser.parse_args(argv)

    reservations: CSV = parse_csv("hotel-reservations.csv")
    if args.cancelled:
        get_cancelled_only(reservations)
        return 0

    top_six_months(reservations.body)
    key_attributes(reservations.body)
    lead_time(reservations.body)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
