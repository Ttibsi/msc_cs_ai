import csv
import heapq
import pandas
from sklearn.model_selection import train_test_split
import sklearn

def clean_data(data: pandas.DataFrame) -> pandas.DataFrame:
    # if the given column's value is -1, we remove it
    data = data[data['age_of_casualty'] != -1].reset_index(drop=True)
    data = data[data['enhanced_casualty_severity'] != -1].reset_index(drop=True)

    # Remove unrequired columns
    data = data.iloc[:, 3:].copy()
    data = data.drop("lsoa_of_casualty", axis=1)

    return data


def main():
    FILE: Final[str] = "dft-road-casualty-statistics-casualty-2024.csv"
    data: pandas.DataFrame = pandas.read_csv(FILE)
    data = clean_data(data)

    with open(FILE) as f:
        headers = [ l.strip().rstrip() for l in f.readlines()[0].split(",") ][3:]

    dependant = data[headers[9]]
    headers.pop(9)
    headers.remove("lsoa_of_casualty")

    results: dict[str, float] = {}

    for independant in headers:
        model = sklearn.linear_model.LinearRegression()
        independant_val = data[[independant]]
        model.fit(independant_val, dependant)

        results[independant] = model.score(independant_val, dependant)

    top_three = heapq.nlargest(3, results.items(), key=lambda y: (y[1], y[0]))
    for k, v in top_three:
        print(f"{k}: {v}")


if __name__ == "__main__":
    raise SystemExit(main())
