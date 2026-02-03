from collections import defaultdict
import random
from typing import TypeAlias

MIN_TEMP = 0.0003
ALPHA = 0.85

cities_t: TypeAlias = dict[str, dict[str, int]]


def parse_data() -> cities_t:
    ret = defaultdict(dict)

    with open("route_finding.csv", "r") as f:
        for idx, line in enumerate(f.readlines()):
            if not line or idx == 0:
                continue
            _from, to, dist = line.strip().replace("\"", "").split(",")

            ret[_from][to] = int(dist)
            ret[to][_from] = int(dist)

    return ret


def path_cost(path: list[str], cities: cities_t) -> int:
    ret = 0
    for idx, elem in enumerate(path):
        if idx == 0:
            continue
        # default value to add is really high to it's never accepted
        ret += cities[path[idx - 1]][elem]
    return ret


def initial_path(cities:cities_t) -> list[str]:
    key = "London"
    while key == "London":
        key = random.choice(list(cities.keys()))

    values = cities[key]
    ret: list[str] = [key]

    while True:
        if not values:
            break

        valid_values = set(x for x in list(values) if x != "London") - set(ret)
        if not valid_values:
            break

        key = random.choice(list(valid_values))
        ret.append(key)
        values = cities[key]

        if len(ret) == len(cities.keys()) - 1:
            # Nowhere left to visit
            break

    return ret


def swap_probability(temp: int, init_cost: int, new_cost: int) -> bool:
    prob: float = (init_cost - new_cost) / temp
    actual = (random.randint(0, 1000) / 10)
    if actual >= prob:
        return True

    return False


def simulated_annealing(path: list[str], cities: cities_t, temp: int) -> str:
    curr_cost = path_cost(path, cities)
    curr_path = path
    idx = random.randint(1, len(path) - 1)

    path = path[:idx]
    key = ""
    values = cities[path[idx - 1]]
    while True:
        if not values:
            break

        valid_values = set(x for x in values if x != "London") - set(path)
        if not valid_values:
            break

        key = random.choice(list(valid_values))
        path.append(key)
        values = cities[key]

        if len(path) == len(cities.keys()) - 1:
            break

    new_path_cost = path_cost(path, cities)

    if new_path_cost <= curr_cost:
        if swap_probability(temp, curr_cost, new_path_cost):
            # If we don't reach the probability threshhold, swap back
            return curr_path

    return path


def path(path: list[str]) -> str:
    text = ""
    for elem in path:
        text += elem[0:3] + " "

    return text


def iterate(cities: cities_t, loop_count: int, temp: int) -> str:
    iter_count = 0
    city_path = initial_path(cities)

    while True:
        iter_count += 1
        city_path = simulated_annealing(city_path, cities, temp)
        temp -= ALPHA

        if city_path[-1] == "":
            city_path = city_path[:-1]
            break

        if temp <= MIN_TEMP:
            break

    cost = path_cost(city_path, cities)
    return f"\u2502 {loop_count} \u2502 {iter_count:>04} \u2502 {cost:>4} \u2502\x1b[36m {path(city_path)}\x1b[0m"


def main() -> int:
    cities: cities_t = parse_data()
    line_len = 100
    temp = 130

    print("\u250C" + ("\u2500" * line_len) + "\u2510")
    headers = "\u2502   \u2502 Iter \u2502 Cost \u2502"
    print(f"{headers}{' ' * (line_len - len(headers))} \u2502")

    for i in range(10):
        temp -= 10
        line = iterate(cities, i, temp)
        print(f"{line}{' ' * (line_len - len(line) + 9)} \u2502")

    print("\u2514" + ("\u2500" * line_len) + "\u2518")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
