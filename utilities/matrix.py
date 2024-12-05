from dataclasses import dataclass
from typing import Any, Iterable


class Matrix:
    pass


@dataclass(frozen=True)
class Matrix:
    elements: list[str]

    def __getitem__(self, coordinates: tuple[int, int]) -> Any:
        i, j = coordinates
        return self.elements[self.max_j - 1 - j][i]

    def get(self, i: int, j: int, default: Any) -> Any:
        return self[i, j] if self.inside(i, j) else default

    def __repr__(self) -> str:
        return '\n'.join(self.elements)

    def inside(self, i, j) -> bool:
        return i in range(self.max_i) and j in range(self.max_j)

    def neighbors(self, i: int, j: int) -> set[tuple[int, int]]:
        return {(x, y) for x, y in [
            (i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1),
            (i, j + 1), (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)
        ] if self.inside(x, y)}

    def to_str(self, indices: Iterable[tuple[int, int]]) -> str:
        return ''.join((self[i, j] for i, j in indices if self.inside(i, j)))

    @property
    def max_i(self) -> int:
        return len(self.elements[0])

    @property
    def max_j(self) -> int:
        return len(self.elements)

    @classmethod
    def from_str(cls, text: str) -> Matrix:
        split = text.split('\n')
        elements = list(map(lambda l: l.strip(), split))
        return Matrix(elements)
