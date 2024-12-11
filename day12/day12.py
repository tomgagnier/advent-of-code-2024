from dataclasses import dataclass
from typing import Self, Iterator, Any, Callable, Iterable

from utilities.unittest import TimedTestCase

NEIGHBOR_OFFSETS = [
    (-1, 0), (0, 1), (1, 0), (0, -1)
]


def neighbors(t: tuple[int, int]) -> Iterator[tuple[int, int]]:
    def add(offset: tuple[int, int]) -> tuple[int, int]:
        return t[0] + offset[0], t[1] + offset[1]

    return map(add, NEIGHBOR_OFFSETS)


def fences(region: Iterable[tuple[int, int]]) -> Iterator[tuple[int, int]]:
    neighborhoods = (list(neighbors(r)) for r in region)
    return (fence for neighborhood in neighborhoods for fence in
            neighborhood if fence not in region)


def count_sides(fences_: Iterable[tuple[int, int]]) -> int:
    count = 0
    for axis0 in range(2):
        axis1 = (axis0 + 1) % 2
        fence_by_axis = sorted(fences_, key=lambda c: (c[axis0], c[axis1]))
        count += 1
        for f0, f1 in zip(fence_by_axis[::2], fence_by_axis[1::2]):
            if f0[axis0] != f1[axis0] or f0[axis1] + 1 != f1[axis1]:
                count += 1
    return count


@dataclass(frozen=True)
class Gardens:
    elements: list[list[str]]

    @classmethod
    def from_file(cls, input_file) -> Self:
        def from_lines(lines: list[str]) -> Self:
            return Gardens([list(list(line.strip())) for line in lines])

        with (open(input_file, 'r') as file):
            return from_lines(file.readlines())

    def __getitem__(self, coordinate: tuple[int, int]) -> str:
        return self.elements[self.max_j - 1 - coordinate[1]][coordinate[0]]

    def __setitem__(self, coordinate: tuple[int, int], value: str) -> None:
        self.elements[self.max_j - 1 - coordinate[1]][coordinate[0]] = value

    def __repr__(self) -> str:
        return '\n'.join([''.join(self.elements[j]) for j in range(self.max_j)])

    def __iter__(self) -> Iterator[tuple[int, int]]:
        for j in range(self.max_j):
            for i in range(self.max_i):
                yield i, j

    def __contains__(self, coordinate: tuple[int, int]) -> bool:
        return 0 <= coordinate[0] < self.max_i and 0 <= coordinate[1] < self.max_j

    @property
    def max_i(self) -> int:
        return len(self.elements[0])

    @property
    def max_j(self) -> int:
        return len(self.elements)

    def get(self, coordinate: tuple[int, int], default: str | None = None) -> Any:
        return self[coordinate] if coordinate in self else default

    def find(self, str_predicate: Callable[[str], bool]) -> None:
        matches = (coordinate for coordinate in self if str_predicate(self[coordinate]))
        first = next(matches, None)
        return first

    def neighbors(self, coordinate: tuple[int, int]) -> Iterator[tuple[int, int]]:
        return (neighbor for neighbor in neighbors(coordinate) if neighbor in self)

    def region(self, start: tuple[int, int]) -> set[tuple[int, int]]:
        def flood_fill(
                members: list[tuple[int, int]], region: set[tuple[int, int]],
        ) -> set[tuple[int, int]]:
            while members:
                member = members.pop()
                region.add(member)
                for neighbor in neighbors(member):
                    if neighbor in self and self[neighbor] == self[
                        start] and neighbor not in region:
                        members.append(neighbor)
            return region

        return flood_fill([start], set())

    def visualize(self, coordinates: Iterable[tuple[int, int]]) -> str:
        visual = [['.' for _ in range(self.max_i)] for _ in range(self.max_j)]
        for (i, j) in coordinates:
            if (i, j) in self:
                visual[self.max_j - 1 - j][i] = 'X'
        return '\n'.join([''.join(row) for row in visual])

    @property
    def regions(self) -> list[list[tuple[int, int]]]:
        visited = set()
        regions = []
        for coordinate in self:
            if coordinate in visited:
                continue
            region = self.region(coordinate)
            visited.update(region)
            regions.append(region)
        return regions

    @property
    def price(self) -> int:
        price = 0
        for region in self.regions:
            fence_count = len(list(fences(region)))
            area = len(region)
            price += fence_count * area
        return price

    @property
    def price2(self) -> int:
        price = 0
        for region in self.regions:
            sides = count_sides(fences(region))
            area = len(region)
            price += sides * area
        return price


example1 = Gardens.from_file('example1.txt')
example2 = Gardens.from_file('example2.txt')
e = Gardens.from_file('e.txt')
gardens = Gardens.from_file('input.txt')


class TestDay12(TimedTestCase):
    def test_region(self):
        assert {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2),
                (4, 3), (4, 4), (3, 4), (2, 4), (2, 3), (2, 2), (2, 1),
                (3, 2), (1, 2), (0, 2), (0, 1), (0, 0), (0, 3), (0, 4),
                (1, 4)} == example1.region((0, 0))

    def test_regions(self):
        assert len(example1.regions) == 5

    def test_fences(self):
        assert 36 == len(list(fences(example1.region((0, 0)))))

    def test_price(self):
        assert 772 == example1.price
        assert 1930 == example2.price
        assert 1377008 == gardens.price

    def test_count_sides(self):
        self.assertEqual(
            len(set(fences(e.region((0, 0))))),
            len(list(fences(e.region((0, 0)))))
        )
        self.assertEqual(12, count_sides(fences(e.region((0, 0)))))
        assert 16 == count_sides(fences(example1.region((0, 0))))

    def test_foo(self):
        self.assertEqual(436, example1.price2)
