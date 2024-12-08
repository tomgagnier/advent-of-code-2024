import re
from dataclasses import dataclass
from itertools import combinations
from typing import Self, Iterator, Callable


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        return Point(self.x - other.x, self.y - other.y)


@dataclass(frozen=True)
class City:
    locations: list[list[str]]

    @classmethod
    def from_file(cls, input_file):
        with (open(input_file, 'r') as file):
            return City.from_lines(file.readlines())

    @classmethod
    def from_lines(cls, lines: list[str]) -> Self:
        return City([list(list(line.strip())) for line in lines])

    def __getitem__(self, p: Point) -> str:
        return self.locations[self.max_y - 1 - p.y][p.x]

    def __iter__(self) -> Iterator[Point]:
        for j in range(self.max_y):
            for i in range(self.max_x):
                yield Point(i, j)

    def __contains__(self, p: Point) -> bool:
        return 0 <= p.x < self.max_x and 0 <= p.y < self.max_y

    @property
    def max_x(self) -> int:
        return len(self.locations[0])

    @property
    def max_y(self) -> int:
        return len(self.locations)


def main(input_file: str) -> None:
    city = City.from_file(input_file)

    antennas = {}
    for point in city:
        feature = city[point]
        if re.match(r'[0-9A-Za-z]', feature):
            if feature not in antennas:
                antennas[feature] = []
            antennas[feature].append(point)

    def anti_nodes(anti_node_finder: Callable[[set[Point], tuple[Point, Point]], None]):
        nodes = set()
        for antenna_locations in antennas.values():
            for antenna_pair in combinations(antenna_locations, 2):
                anti_node_finder(nodes, antenna_pair)
        return nodes

    def part1(nodes:set[Point], antenna_pair:tuple[Point, Point]) -> None:
        for i in [0, 1]:
            anti_node = antenna_pair[i] + antenna_pair[i] - antenna_pair[(i + 1) % 2]
            if anti_node in city:
                nodes.add(anti_node)

    def part2(nodes:set[Point], antenna_pair:tuple[Point, Point]) -> None:
        for i in [0, 1]:
            anti_node = antenna_pair[i]
            while anti_node in city:
                nodes.add(anti_node)
                anti_node += antenna_pair[i] - antenna_pair[(i + 1) % 2]

    print(input_file)
    print('    part1: ', len(anti_nodes(part1)))
    print('    part2: ', len(anti_nodes(part2)))


main('example.txt')
main('input.txt')
