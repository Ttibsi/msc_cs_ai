import csv
import uuid

def invalid(field: str) -> bool:
    return (not field or field.lower() in ["null", "none", "0"])


def main() -> int:
    with open("PeoplesFavourites.csv") as f:
        data = f.readlines()
        headers = data[0].strip().split(",")
        rest = [x.strip().split(",") for x in data[1:]]

    assert headers[11] == "First Name"
    assert headers[12] == "Last Name"
    assert headers[13] == "Email"

    copy = rest
    for idx, row in enumerate(rest):
        # remove rows with invalid first/last/email fields
        if any([invalid(x) for x in row[11:]]):
            copy[idx] = []
            continue

        # anonymise data
        copy[idx][11] = uuid.uuid4()
        del copy[idx][12]

        # remove null values
        for idy, cell in enumerate(row):
            if cell in ["", "null", "none", "0"]:
                copy[idx][idy] = "NULL"

    # Write to file
    with open("clean_file.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for row in copy:
            if row:
                writer.writerow(row)

    return 0

if __name__ == '__main__':
    raise SystemExit(main())
