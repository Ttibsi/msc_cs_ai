from collections import defaultdict
import random
from typing import TypeAlias

cities_t: TypeAlias = dict[str, dict[str, int]]

def parse_data() -> cities_t:
    """
    Transform the input data into a format we can manipulate

    Returns: dict[str, dict[str, int]]
    """
    dataset = defaultdict(dict)

    with open("route_finding.csv", "r") as f:
        for idx, line in enumerate(f.readlines()):
            if not line or idx == 0:
                continue
            _from, to, dist = line.strip().replace("\"", "").split(",")

            dataset[_from][to] = int(dist)
            dataset[to][_from] = int(dist)

     return dataset


def steepest_ascent(cities: cities_t, key: str, path: list[str]) -> str:
    """
    Select the best city to traverse to next

    Returns: str - the name of the city to add to the path
    """
    remaining_elems = {k:v for k, v in cities[key].items() if k != "London" and k not in path}
    if not remaining_elems:
        return ""
    return min(remaining_elems, key=remaining_elems.get)


def path_cost(path: list[str], cities: cities_t) -> int:
    """
    Traverse the dataset and calculate a path's cost

    Returns: int - the cost of the path
    """
    cost = 0
    for idx, elem in enumerate(path):
        if idx == 0:
            continue

        cost += cities[path[idx - 1]][elem]

    return cost


def path(path: list[str]) -> str:
    """ Take a path of cities and return a displayable string """
    text = ""
    for elem in path:
        text += elem[0:3] + " "

    return text[:-1]


def iterate(cities: cities_t, loop_count: int) -> str:
    """
    A single run of our algorithm.

    Returns: str - a string "report" to display
    """
    iter_count = 0
    total_iters = 0

    city_path = [random.choice(list(cities.keys()))]
    while city_path[0] == "London":
        city_path[0] = random.choice(list(cities.keys()))

    while True:
        total_iters += 1
        city_path.append(steepest_ascent(cities, city_path[-1], city_path))

        if city_path[-1] == "":
            city_path = city_path[:-1]
            break

        iter_count += 1
        if iter_count == 100:
            break

    cost = path_cost(city_path, cities)
    div = "\x1b[0m\u2502\x1b[32m "
    return f"{div}{loop_count} {div}Iterations: {total_iters:>02} {div}Total cost: {cost:>03} {div.replace('2','6')}{path(city_path)}\x1b[0m"


def main() -> int:
    cities: cities_t = parse_data()
    line_len = 90 

    print("\u250C" + ("\u2500" * line_len) + "\u2510")
    for i in range(10):
        line = iterate(cities, i)
        print(f"{line}{' ' * (line_len - len(line) + 40)} \u2502")
    print("\u2514" + ("\u2500" * line_len) + "\u2518")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
