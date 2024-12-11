import textwrap
from dataclasses import dataclass
from typing import Any, Iterator, Self, Callable

NEIGHBOR_OFFSETS = [
    (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)
]

def neighbors(t: tuple[int, int]) -> Iterator[tuple[int, int]]:
    def add(offset: tuple[int, int]) -> tuple[int, int]:
        return t[0] + offset[0], t[1] + offset[1]

    return map(add, [(-1, 0), (0, 1), (1, 0), (0, -1)])


@dataclass(frozen=True, eq=True)
class Coordinate:
    ij: tuple[int, int]

    @classmethod
    def from_tuples(cls, *tuples: tuple[int, int]) -> list[Self]:
        return [Coordinate(t) for t in tuples]

    @property
    def i(self) -> int:
        return self.ij[0]

    @property
    def j(self) -> int:
        return self.ij[1]

    def __getitem__(self, index: int) -> int:
        return self.ij[index]

    def __add__(self, other: Self | tuple[int, int]) -> Self:
        return Coordinate((self[0] + other[0], self[1] + other[1]))

    def __sub__(self, other: Self | tuple[int, int]) -> Self:
        return Coordinate((self[0] - other[0], self[1] - other[1]))

    def __repr__(self) -> str:
        return str(self.ij)

    def __eq__(self, other: Self | tuple[int, int]) -> bool:
        return isinstance(other, Coordinate) and self.ij == other.ij or self.ij == other

    def translate(self, coordinates: list[Self | tuple[int, int]]) -> Iterator[Self]:
        return map(lambda c: c + self, coordinates)

    def neighbors(self) -> Iterator[Self]:
        return map(lambda c: self + c, NEIGHBOR_OFFSETS)



@dataclass(frozen=True)
class StringMatrix:
    elements: list[list[str]]

    @classmethod
    def from_lines(cls, lines: list[str]) -> Self:
        return StringMatrix([list(list(line.strip())) for line in lines])

    @classmethod
    def from_multiline_str(cls, text: str) -> Self:
        return StringMatrix.from_lines(textwrap.dedent(text).strip().split('\n'))

    @classmethod
    def from_file(cls, input_file):
        with (open(input_file, 'r') as file):
            return StringMatrix.from_lines(file.readlines())

    def __getitem__(self, coordinate: Coordinate | tuple[int, int]) -> str:
        return self.elements[self.max_j - 1 - coordinate[1]][coordinate[0]]

    def __setitem__(self, coordinate: Coordinate | tuple[int, int], value: str) -> None:
        self.elements[self.max_j - 1 - coordinate[1]][coordinate[0]] = value

    def __repr__(self) -> str:
        return '\n'.join([''.join(self.elements[j]) for j in range(self.max_j)])

    def __iter__(self) -> Iterator[Coordinate]:
        for j in range(self.max_j):
            for i in range(self.max_i):
                yield Coordinate((i, j))

    def __contains__(self, coordinate: Coordinate) -> bool:
        return 0 <= coordinate[0] < self.max_i and 0 <= coordinate[1] < self.max_j

    @property
    def max_i(self) -> int:
        return len(self.elements[0])

    @property
    def max_j(self) -> int:
        return len(self.elements)

    def get(self, coordinate: Coordinate | tuple[int, int], default: str | None = None) -> Any:
        return self[coordinate] if coordinate in self else default

    def find(self, str_predicate: Callable[[str], bool]) -> Coordinate | None:
        matches = (coordinate for coordinate in self if str_predicate(self[coordinate]))
        first = next(matches, None)
        return first

    def neighbors(self, coordinate: Coordinate) -> Iterator[Coordinate]:
        return (neighbor for neighbor in coordinate.neighbors() if neighbor in self)
