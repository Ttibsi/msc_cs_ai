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


# r^2 = (Ypred - mean) ^2 / (Y - mean) ^ 2
def best_fit(mean: float, pred: float, y: float) -> float:
    top = math.pow(pred - mean, 2)
    bottom = math.pow(y - mean, 2)
    return top / bottom


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
def linear_regression(data: list[Datum], mask: tuple[int, ...]) -> tuple[list[float], float]:
    sum_bee_pop = sum([x.bee_occupancy for x in data])
    sum_ivs = sum([x.ivs(mask) for x in data])
    c = 1.2

    points: list[float] = []
    ys = []
    for idx, datum in enumerate(data):
        x = datum.bee_occupancy
        y = datum.ivs(mask)
        ys.append(y)

        x_bias = x - sum_bee_pop
        y_bias = y - sum_ivs 
        numerator = x_bias * y_bias
        denominator = math.pow(x_bias, 2)
        m = numerator / denominator

        c = y - ((sum_bee_pop / len(data)) * m)

        total = c + (m * x)
        points.append(total)

    residual = mean_squared_error(points, ys)
    return points, residual


def compare(result: list[float], best: list[float]) -> bool:
    return sum(result) < sum(best)
    return (sum(result) / len(result)) < (sum(best) / len(best))


def hill_walk(data: list[Datum]) -> tuple[int, ...]:
    # Generate every possible mask
    masks = itertools.product([0, 1], repeat=5)
    next(masks)  # Skip all 0s

    best: float = 0.0
    best_mask: tuple[int, ...] = []
    counter = 0
    for m in masks:
        result, residual = linear_regression(data, m)
        if not best or residual < best:
            best = residual 
            best_mask = m
            counter += 1

    return best_mask


def draw_line_graph(data: list[Datum], mask: tuple[int, ...]):
    result, residual = linear_regression(data, mask)
    plt.plot(result, "ro", label="data points")
    plt.legend()
    plt.show()


def main() -> int:
    data: list[Datum] = process_csv()
    best_predictors = hill_walk(data)
    print(best_predictors)

    # draw the best chart on the screen?
    draw_line_graph(data, best_predictors)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
