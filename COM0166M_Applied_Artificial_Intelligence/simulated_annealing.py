#!/usr/bin/python3
import math
import random
import sys
from typing import NamedTuple

data = """
2.7933,3.694
2.6067,4.4254
2.86,5.0373
2.54,6.2463
3.1267,6.4701
3.7267,6.8881
4.4867,7.4403
5.5533,7.4254
6.3,7.3955
7.6333,6.9179
7.22,6.3955
6.6333,5.8284
7.0867,5.1269
7.4733,4.4701
7.18,3.709
6.6867,2.8284
6.2067,2.0522
5.54,1.8731
5.1533,2.3358
4.9667,3.0075
4.8867,3.5448
4.2733,3.2313
3.6333,2.7537
2.9933,2.8433
"""


class Coordinate(NamedTuple):
    x: float
    y: float

    def distance(self, other) -> float:
        x_half = math.pow(other.x - self.x, 2)
        y_half = math.pow(other.y - self.y, 2)
        return round(math.sqrt(x_half + y_half), 2)


def parse_data() -> list[Coordinate]:
    ret = []
    for line in data.split("\n"):
        if not line:
            continue
        x, y = line.split(",")
        ret.append(Coordinate(float(x), float(y)))

    return ret


def path_cost(cities: list[Coordinate]) -> float:
    total = 0.0

    for idx, elem in enumerate(cities):
        if idx == 0:
            continue

        total += cities[idx - 1].distance(elem)

    return float(f"{total:05.2f}")


def probable_swap(cities: list[Coordinate], initial_cost: int, temp: int) -> bool:
    prob: float = (initial_cost - path_cost(cities)) / temp
    actual = random.randint(0, 1000) / 10
    if actual >= prob:
        return True

    return False


def simulated_annealling(cities: list[Coordinate], temp: int) -> list[Coordinate]:
    idx = random.randint(1, len(cities) - 1)
    cities[idx], cities[idx - 1] = cities[idx - 1], cities[idx]

    if not probable_swap(cities, path_cost(cities), temp):
        # If we don't reach the probability threshhold, swap back
        cities[idx], cities[idx - 1] = cities[idx - 1], cities[idx]

    return cities


def main() -> int:
    cities = parse_data()
    random.shuffle(cities)
    line_len = 23

    temp = 10.00
    min_temp = 0.00005
    alpha = 0.795

    if len(sys.argv) == 3:
        temp = float(sys.argv[1])
        min_temp = float(sys.argv[2])

    print("\u250C" + ("\u2500" * line_len) + "\u2510")
    print(f"\u2502 Temp: {temp}            \u2502")
    print(f"\u2502 Threshold: {min_temp:.5f}    \u2502")
    print(f"\u2502 Alpha: {alpha}          \u2502")
    print("\u2502" + ("\u2500" * line_len) + "\u2502")
    print(f"\u2502 \x1b[7mIters\x1b[27m \u2502 \x1b[7mCost\x1b[27m  \u2502 \x1b[7mTemp\x1b[27m  \u2502")

    iter_count = 0
    while True:
        iter_count += 1
        cities = simulated_annealling(cities, temp)
        print(f"\u2502 {iter_count:>5d} \u2502 {path_cost(cities):.2f} \u2502 {temp:05.2f} \u2502")
        temp -= alpha

        if temp <= min_temp:
            break
    print("\u2514" + ("\u2500" * line_len) + "\u2518")


if __name__ == "__main__":
    raise SystemExit(main())
