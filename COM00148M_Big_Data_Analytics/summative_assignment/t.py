import csv
import pandas
from sklearn.model_selection import train_test_split
import sklearn

def clean_data(data: pandas.DataFrame) -> pandas.DataFrame:
    # if the given column's value is -1, we remove it
    data = data[data['age_of_casualty'] != -1].reset_index(drop=True)
    data = data[data['enhanced_casualty_severity'] != -1].reset_index(drop=True)

    return data


def main():
    data: pandas.DataFrame = pandas.read_csv("dft-road-casualty-statistics-casualty-2024.csv")
    data = clean_data(data)


if __name__ == "__main__":
    raise SystemExit(main())
