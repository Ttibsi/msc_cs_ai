import sys
import math
from typing import NamedTuple
import random

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

    return total


def steepest_ascent(cities: list[Coordinate]) -> list[Coordinate]:
    initial_cost = path_cost(cities)
    initial_cities = cities

    for idx, elem in enumerate(cities):
        if idx == 0:
            continue

        cities[idx], cities[idx - 1] = cities[idx - 1], elem
        if path_cost(cities) < initial_cost:
            return cities

    return initial_cities


def iteration(cities: list[Coordinate], loop_count: int) -> int:
    total_iters = 0
    iter_count = 0
    cost = path_cost(cities)
    while True:
        cities = steepest_ascent(cities)
        iter_cost = path_cost(cities)
        total_iters += 1

        if iter_cost >= cost:
            iter_count += 1

            if iter_count == 100:
                break
        else:
            cost = iter_cost
            iter_count = 0

    print(f"\u2502 {loop_count} \u2502 Iterations: {total_iters} \u2502 Total cost: {cost:.3f} \u2502")
    return total_iters


def main() -> int:
    loop_count = 10
    if len(sys.argv) == 3:
        if sys.argv[1] == "-n":
            loop_count = int(sys.argv[2])

    cities = parse_data()
    line_len = 42
    total_iters = 0

    print("\u250C" + ("\u2500" * line_len) + "\u2510")

    for i in range(loop_count):
        # Initial order using the random approach
        random.shuffle(cities)
        total_iters += iteration(cities, i)

    print("\u2514" + ("\u2500" * line_len) + "\u2518")
    print(f"Total iterations: {total_iters}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
