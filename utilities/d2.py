import textwrap
from dataclasses import dataclass
from typing import Any, Iterator, Self, Callable


@dataclass(frozen=True)
class Matrix:
    elements: list[list[str]]

    @classmethod
    def from_lines(cls, lines: list[str]) -> Self:
        return Matrix([list(list(line.strip())) for line in lines])

    @classmethod
    def from_multiline_str(cls, text: str) -> Self:
        return Matrix.from_lines(textwrap.dedent(text).strip().split('\n'))

    def __getitem__(self, coordinates: tuple[int, int]) -> str:
        return self.elements[self.max_j - 1 - coordinates[1]][coordinates[0]]

    def __setitem__(self, coordinates: tuple[int, int], value: str) -> None:
        self.elements[self.max_j - 1 - coordinates[1]][coordinates[0]] = value

    def __repr__(self) -> str:
        return '\n'.join([''.join(self.elements[j]) for j in range(self.max_j)])

    def __iter__(self) -> Iterator[tuple[int, int]]:
        for j in range(self.max_j):
            for i in range(self.max_i):
                yield i, j

    def __contains__(self, coordinates: tuple[int, int]) -> bool:
        return 0 <= coordinates[0] < self.max_i and 0 <= coordinates[1] < self.max_j

    @property
    def max_i(self) -> int:
        return len(self.elements[0])

    @property
    def max_j(self) -> int:
        return len(self.elements)

    def get(self, coordinates: tuple[int, int], default: str | None = None) -> Any:
        return self[coordinates] if coordinates in self else default

    def find(self, predicate: Callable[[str], bool]) -> tuple[int, int] | None:
        matches = (coordinate for coordinate in self if predicate(self[coordinate]))
        return next(matches, None)

    def neighbors(self, coordinates: tuple[int, int]) -> list[tuple[int, int]]:
        i, j = coordinates
        return [neighbor for neighbor in [
            (i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j + 1),
            (i + 1, j + 1), (i + 1, j), (i + 1, j - 1), (i, j - 1)
        ] if neighbor in self]
