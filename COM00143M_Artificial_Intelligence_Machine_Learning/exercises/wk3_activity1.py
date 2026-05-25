from typing import Final
from queue import Queue

heuristics: Final[dict[str, int]] = {
    'A': 5,
    'B': 6,
    'C': 8,
    'D': 4,
    'E': 4,
    'F': 5,
    'G': 2,
    'H': 0,
}

connections: Final[dict[str, list[str]]] = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A", "F"],
    "D": ["B", "E"],
    "E": ["D", "F", "G"],
    "F": ["C", "E", "G"],
    "G": ["E", "F", "H"],
    "H": ["G"],
}

def steps(start: str, end: str) -> int:
    if start == "A" and end == "B":
        return 3
    if start == "A" and end == "C":
        return 3
    if start == "B" and end == "D":
        return 2
    if start == "C" and end == "F":
        return 3
    if start == "D" and end == "E":
        return 4
    if start == "E" and end == "F":
        return 1
    if start == "E" and end == "G":
        return 2
    if start == "F" and end == "G":
        return 3
    if start == "G" and end == "H":
        return 2

    return 1000


def greedy_best_first_search() -> None:
    visited = ["A"]
    q = ["A"]

    while "H" not in visited:
        neighbors = connections[visited[-1]]

        distance = 100
        desired_neighbor = "z"
        for n in neighbors:
            if n in visited:
                continue
            if heuristics[n] < distance:
                distance = heuristics[n]
                desired_neighbor = n

        visited.append(desired_neighbor)
            
    print(f"Greedy Best-first Search: {visited}")


def astar() -> None:
    visited = ["A"]
    q = ["A"]

    while "H" not in visited:
        neighbors = connections[visited[-1]]

        values = {n: 0 for n in neighbors}
        for n in neighbors:
            if n in visited:
                values.pop(n)
                continue

            value = heuristics[n] + steps(visited[-1], n)
            if value > 1000:
                value = heuristics[n] + steps(n, visited[-1])
                if value > 1000:
                    raise AssertionError(f"ERROR: {visited[-1]} | {n}")

            values[n] = value

        visited.append(min(values, key=values.get))

    print(f"A-star: {visited}")


def main() -> int:
    greedy_best_first_search()
    astar()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
