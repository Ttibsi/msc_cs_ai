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


def get_minimum(nodes: list[str]) -> str:
    min_val = 1000
    min_node = 'Z'
    for node in nodes:
        if heuristics[node] < min_val:
            min_node = node

    return min_node


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
    ...

def main() -> int:
    greedy_best_first_search()
    astar()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
