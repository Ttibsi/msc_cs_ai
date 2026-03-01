import itertools
import math
from dataclasses import dataclass

@dataclass
class Datum:
    year: int
    scheme_coverage: float
    bee_occupancy: float
    hoverfly_occupancy: float
    woodland_butterfly_occupancy: float
    farmland_butterfly_occupancy: float
    birds: float | None = None

    def ivs(self, mask: list[int]) -> float:
        values = [
            self.scheme_coverage if mask[0] else 0.0,
            self.hoverfly_occupancy if mask[1] else 0.0,
            self.woodland_butterfly_occupancy if mask[2] else 0.0,
            self.farmland_butterfly_occupancy if mask[3] else 0.0,
            self.birds if self.birds is not None and mask[4] else 0.0
        ]

        return sum(values)


def process_csv() -> list[Datum]:
    data: list[Datum] = []

    with open("preprocessed_data.csv", "r") as f:
        lines = f.readlines()
        for idx, line in enumerate(lines):
            if idx == 0:
                continue
            # We need to be sure that the birds field is populated correctly, as
            # there may be no value in that column
            parts = line.rstrip().split(",")

            # Transform the strings from the CSV file into the right data types
            parts[0] = int(parts[0])
            if parts[-1] == "":
                parts[-1] = None

            for idx, elem in enumerate(parts[1:], start=1):
                parts[idx] = float(elem) if elem is not None else None
            datum = Datum(*parts)
            data.append(datum)

    return data


def calculate_bias(actual: float, expected: float) -> float:
    return actual - expected


# r^2 = (Ypred - mean) ^2 / (Y - mean) ^ 2
def best_fit(mean: float, pred: float, y: float) -> float:
    top = math.pow(pred - mean, 2)
    bottom = math.pow(y - mean, 2)
    return (top / bottom) 


# y = c + (m * x)
# x = input data points
# c = intercept - the point where the estimated regression line crosses the y axis
# m = bias/slope of the regression line
def linear_regression(data: list[Datum], mask: list[int]) -> list[float]:
    mean_bee_pop = sum([x.bee_occupancy for x in data]) / len(data)
    mean_ivs = sum([x.ivs(mask) for x in data]) / len(data)
    c = 0.1

    sum_total = 0
    fits = [False] * len(data)
    ys = [0.0] * len(data)
    for idx, datum in enumerate(data):
        x = datum.bee_occupancy
        y = datum.ivs(mask)
        ys[idx] = y

        x_bias = calculate_bias(x, mean_bee_pop)
        bias = x_bias * calculate_bias(y, mean_ivs)
        m = bias / math.pow(x_bias, 2)

        total = c + (m * x)
        sum_total += total

    regressions: list[float] = []
    for y in ys:
        r_squared = best_fit(sum_total, sum(ys), y)
        regressions.append(r_squared)

    # Return the mean of the r_squared calculation
    return regressions


def compare(result: list[float], best: list[float]) -> bool:
    return (sum(result) / len(result)) > (sum(best) / len(best))


def hill_walk(data: list[Datums]) -> list[int]:
    # Generate every possible mask
    masks = itertools.product([1, 0], repeat=5)

    best: list[float] = [0,0,0,0,0]
    best_mask: list[int] = []
    counter = 0
    for m in masks:
        result = linear_regression(data, m)
        if compare(result, best):
            best = result
            best_mask = m
            counter += 1

            if counter == 3:
                return best_mask

    return [0,0,0,0,0]


def display_best(preds: list[int]) -> None:
    ret = ""

    if preds[0]:
        ret += "scheme_coverage, "
    if preds[1]:
        ret += "hoverfly_occupancy, "
    if preds[2]:
        ret += "woodland_butterfly_occupancy, "
    if preds[3]:
        ret += "farmland_butterfly_occupancy, "
    if preds[4]:
        ret += "birds, "

    return ret

def main() -> int:
    data: list[Datum] = process_csv()
    best_predictors = hill_walk(data)
    print(display_best(best_predictors))

    # draw the best chart on the screen?
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
