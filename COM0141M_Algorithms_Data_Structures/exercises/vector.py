from __future__ import annotations

import copy
import math

"""
Week 4 exercises - implement a Vector typr
"""


class Vector:
    _vector: list[float]

    def __init__(self, data: list[float]):
        self._vector = copy.deepcopy(data)

    def __str__(self) -> str:
        return str(self._vector).replace('[', '<').replace(']', '>')

    def __repr__(self) -> str:
        return str(self)

    def dim(self) -> int:
        return len(self._vector)

    def get(self, index: int) -> float:
        if index > self.dim() - 1:
            raise ValueError("Index not found")
        return self._vector[index]

    def set(self, index: int, value: float) -> None:
        if index > self.dim() - 1:
            raise ValueError("Index not found")

        self._vector[index] = value

    def scalar_product(self, scalar: float) -> Vector:
        return Vector([x * float(scalar) for x in self._vector])

    def add(self, other: Vector) -> Vector | None:
        if not isinstance(other, Vector):
            return None
        if self.dim() != other.dim():
            return None

        return Vector([
            self.get(i) + other.get(i)
            for i in range(self.dim())
        ])

    def equals(self, other: Vector) -> bool:
        if not isinstance(other, Vector):
            return False

        if self.dim() != other.dim():
            return False

        for i in range(self.dim()):
            if not math.isclose(self.get(i), other.get(i)):
                return False

        return True

    def __eq__(self, other: object) -> bool:
        return self.equals(other)

    def __ne__(self, other: object) -> bool:
        return not self.equals(other)

    def __add__(self, other: Vector) -> Vector | None:
        return self.add(other)

    def __mul__(self, scalar: float):
        return self.scalar_product(scalar)

    def __rmul__(self, scalar: float) -> Vector:
        return self.scalar_product(scalar)

    def __iadd__(self, other: Vector):
        # This will tell python to instead try __add__
        return NotImplemented

    def __imul__(self, scalar: float):
        return NotImplemented
