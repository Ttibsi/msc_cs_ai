import random
from collections import defaultdict

def parse_data() -> list[Edge]:
    ret = defaultdict(dict)

    with open("route_finding.csv", "r") as f:
        for idx, line in enumerate(f.readlines()):
            if not line or idx == 0:
                continue
            _from, to, dist = line.strip().replace("\"", "").split(",")

            ret[_from][to] = int(dist)
            ret[to][_from] = int(dist)

    return ret


def steepest_ascent(cities, key, path) -> str:
    remaining_elems = {k:v for k, v in cities[key].items() if k not in path}
    if not remaining_elems:
        return ""
    return max(remaining_elems, key=remaining_elems.get)


def path_cost(path: list[str], cities: dict[str, dict[str, int]]) -> int:
    ret = 0
    for idx, elem in enumerate(path):
        if idx == 0:
            continue

        ret += cities[path[idx - 1]][elem]

    return ret

def iterate(cities, loop_count: int) -> None:
    iter_count = 0
    total_iters = 0

    city_path = [random.choice(list(cities.keys()))]
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
    print(f"\u2502\x1b[32m {loop_count} \u2502 Iterations: {total_iters:>02} \u2502 Total cost: {cost:>04} \x1b[0m\u2502")
    return


def main() -> int:
    cities = parse_data()
    line_len = 39 

    print("\u250C" + ("\u2500" * line_len) + "\u2510")
    for i in range(10):
        iterate(cities, i)
    print("\u2514" + ("\u2500" * line_len) + "\u2518")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
