import csv
import heapq
import itertools
import time
import timeit
from typing import Final

import numpy
import matplotlib.pyplot as plt
import pandas
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

FILE: Final[str] = "dft-road-casualty-statistics-casualty-2024.csv"

def clean_data(data: pandas.DataFrame) -> pandas.DataFrame:
    # if the given column's value is -1, we remove it
    data = data[data['age_of_casualty'] != -1].reset_index(drop=True)
    data = data[data['enhanced_casualty_severity'] != -1].reset_index(drop=True)

    return data

def most_likely_candidates(data: pandas.DataFrame):
    cols_to_drop: Final[list[str]] = [
        "collision_index",
        "collision_year",
        "collision_ref_no", 
        "vehicle_reference",
        "casualty_reference",
        "lsoa_of_casualty",
        "age_band_of_casualty",
        "casualty_severity",
    ]

    data = clean_data(data)
    data = data.drop(columns=cols_to_drop)

    with open(FILE) as f:
        headers = [ l.strip().rstrip() for l in f.readlines()[0].split(",") ][3:]

    dependant = data[headers[9]]
    headers.pop(9)
    headers = [x for x in headers if x not in cols_to_drop]

    results: dict[str, float] = {}

    for independant in headers:
        model = sklearn.linear_model.LinearRegression()
        independant_val = data[[independant]]
        model.fit(independant_val, dependant)

        results[independant] = model.score(independant_val, dependant)

    top_three = heapq.nlargest(3, results.items(), key=lambda y: (y[1], y[0]))
    print("Top 3 variables: ")
    for k, v in top_three:
        print(f"{k}: {v:.4f}")

    print("\nAll results:")
    sorted_results = {k:v for k, v in reversed(sorted(results.items(), key=lambda item: item[1]))}
    for k, v in sorted_results.items():
        print(f"{k}: {v:.4f}")


def investigate_relationships(data: pandas.DataFrame):
    fields = ["casualty_severity", "age_of_casualty", "casualty_type"]
    # data = clean_data(data)
    data = data[fields].copy()

    results: dict[tuple[str, str], float] = {}
    print("Correlation:")
    print(data[fields].corr()["casualty_type"])

    # for f1, f2 in itertools.permutations(fields, 2):
    #     if (f2, f1) in results.keys():
    #         continue
    #     results[(f1, f2)] = data[f1].corr(data[f2])
    #
    # print("Correlation data:")
    # for k, v in results.items():
    #     print(f"{k}: {v:.4f}")


# Multiple Linear Regression
def demographics(data: pandas.DataFrame):
    fields = ["casualty_severity", "age_of_casualty", "sex_of_casualty"]
    data = clean_data(data)
    data = data[fields].copy()

    dependant = pandas.concat(
        [data["age_of_casualty"], pandas.get_dummies(data["sex_of_casualty"])],
        axis=1
    )
    dependant.columns = dependant.columns.astype(str)
    independant = data[["casualty_severity"]]

    x_train, x_test, y_train, y_test = train_test_split(
        dependant, independant, random_state=0, test_size=0.3
    )

    model = sklearn.linear_model.LinearRegression()
    model.fit(x_train, y_train)
    
    result = model.score(x_test, y_test)
    print(f"Rate of demographic characteristics as predictors of severity: {result:.4f}")
    print()


def other_attributes(data: pandas.DataFrame):
    data = data[data["casualty_severity"] != 1].reset_index(drop=True)
    data = data[data['casualty_severity'] != -1].reset_index(drop=True)
    data = clean_data(data)
    
    y = data["casualty_severity"]
    cols_to_drop: Final[list[str]] = [
        "collision_index",
        "collision_year",
        "collision_ref_no", 
        "vehicle_reference",
        "casualty_reference",
        "lsoa_of_casualty",
        "casualty_adjusted_severity_serious",
        "casualty_adjusted_severity_slight",
        "enhanced_casualty_severity"
    ]
    data = data.drop(columns=cols_to_drop + ['casualty_severity'])

    data = pandas.get_dummies(data, columns=['sex_of_casualty', 'pedestrian_location'])

    tree = DecisionTreeClassifier()
    tree.fit(data, y)

    importances = pandas.Series(tree.feature_importances_, index=data.columns)
    top_three = importances.sort_values(ascending=False).head(3)

    print("Top 3 Indicators:")
    for idx, val in top_three.items():
        print(f"{idx}: {val:.4f}")


def main():
    data: pandas.DataFrame = pandas.read_csv(FILE)

    start = time.time()
    most_likely_candidates(data)
    first = time.time()
    print(f"Time: {first - start}\n")

    investigate_relationships(data)
    second = time.time()
    print(f"Time: {second - first}\n")

    demographics(data)
    other_attributes(data)
    third = time.time()
    print(f"Time: {third - second}")


def main2():
    data: pandas.DataFrame = pandas.read_csv(FILE)
    print(f"Age is -1: {(data['age_of_casualty'] == -1).sum()}")
    print(f"enhanced_casualty_severity is -1: {(data['enhanced_casualty_severity'] == -1).sum()}")

if __name__ == "__main__":
    raise SystemExit(main())
