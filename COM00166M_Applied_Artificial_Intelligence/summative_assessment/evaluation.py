from dataclasses import dataclass
from typing import Sequence
import itertools
import math

import matplotlib.pyplot as plt


@dataclass
class Datum:
    year: int
    scheme_coverage: float
    bee_occupancy: float
    hoverfly_occupancy: float
    woodland_butterfly_occupancy: float
    farmland_butterfly_occupancy: float
    birds: float | None = None

    def ivs(self, mask: tuple[int, ...]) -> float:
        values = [
            self.scheme_coverage if mask[0] else 0.0,
            self.hoverfly_occupancy if mask[1] else 0.0,
            self.woodland_butterfly_occupancy if mask[2] else 0.0,
            self.farmland_butterfly_occupancy if mask[3] else 0.0,
            self.birds if self.birds is not None and mask[4] else 0.0
        ]

        return sum(values) / len(values)


def process_csv() -> list[Datum]:
    data: list[Datum] = []

    with open("preprocessed_data.csv", "r") as f:
        lines = f.readlines()
        for idx, line in enumerate(lines):
            if idx == 0:
                continue
            # We need to be sure that the birds field is populated correctly, as
            # there may be no value in that column
            parts: Sequence[str | int | float] = line.rstrip().split(",")

            # Transform the strings from the CSV file into the right data types
            parts[0] = int(parts[0])
            if parts[-1] == "":
                parts[-1] = None

            for idx, elem in enumerate(parts[1:], start=1):
                parts[idx] = float(elem) if elem is not None else None
            datum = Datum(*parts)
            data.append(datum)

    return data


def mean_squared_error(points: list[float], ys: list[float]) -> float:
    return sum(
        math.pow(ys[idx] - points[idx], 2)
        for idx in range(len(points))
    ) / len(points)


# y = c + (m * x)
# x = input data points
# c = intercept - the point where the estimated regression line crosses the y axis
# m = bias/slope of the regression line
# https://medium.com/geekculture/linear-regression-from-scratch-in-python-without-scikit-learn-a06efe5dedb6
def linear_regression(data: list[Datum], mask: tuple[int, ...]) -> tuple[list[float], list[float], float]:
    ys = [x.ivs(mask) for x in data]
    mean_bee_pop = sum([x.bee_occupancy for x in data]) / len(data)
    mean_ivs = sum(ys) / len(data)

    numerator = sum(
        (data[i].bee_occupancy - mean_bee_pop) * (ys[i] - mean_ivs)
        for i in range(len(data))
    )
    denominator = sum([math.pow(x.bee_occupancy - mean_bee_pop, 2) for x in data])
    m = numerator / denominator
    c = mean_ivs - (m * mean_bee_pop)
    predicted_y = [m * x.bee_occupancy + c for x in data]
    return predicted_y, ys, mean_squared_error(predicted_y, ys)


def hill_walk(data: list[Datum]) -> tuple[int, ...]:
    # Generate every possible mask
    masks = itertools.product([0, 1], repeat=5)
    next(masks)  # Skip all 0s

    best_mse: float = math.inf
    best_mask: tuple[int, ...] = []
    counter = 0
    for m in masks:
        _, _, mse = linear_regression(data, m)
        print(f"  | MSE:{mse:05.2f}, best:{best_mse:05.2f}, mask = {m} | ")
        if mse < best_mse:
            best_mse = mse 
            best_mask = m
            counter += 1

    return best_mask


def draw_line_graph(data: list[Datum], mask: tuple[int, ...]):
    results, ys, _ = linear_regression(data, mask)

    x_list = list(range(1992, 2023))
    plt.plot(x_list, results, label="Regression line")
    plt.plot(x_list, ys, "ro", label="IVs (mean)")
    plt.xlabel("Year")
    plt.ylabel("Change in Bee population")

    plt.legend()
    plt.savefig("chart.png")
    plt.show()


def main() -> int:
    data: list[Datum] = process_csv()
    best_predictors = hill_walk(data)
    draw_line_graph(data, best_predictors)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
