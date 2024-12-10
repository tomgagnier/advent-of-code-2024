import re
import unittest
from dataclasses import dataclass
from typing import Self, Iterator


def neighbors(t: tuple[int, int]) -> Iterator[tuple[int, int]]:
    def add(offset: tuple[int, int]) -> tuple[int, int]:
        return t[0] + offset[0], t[1] + offset[1]

    return map(add, [(-1, 0), (0, 1), (1, 0), (0, -1)])


@dataclass(frozen=True)
class Topology:
    elevations: list[list[int]]

    @property
    def end_of_i(self) -> int:
        return len(self.elevations[0])

    @property
    def end_of_j(self) -> int:
        return len(self.elevations)

    @classmethod
    def from_lines(cls, lines: list[str]) -> Self:
        number_matches = [re.findall(r'\d', l) for l in lines]
        ints = [[int(value) for value in match] for match in number_matches]
        return Topology(ints)

    @classmethod
    def from_file(cls, input_file):
        with (open(input_file, 'r') as file):
            return Topology.from_lines(file.readlines())

    def __getitem__(self, coordinate: tuple[int, int]) -> int:
        return self.elevations[self.end_of_j - 1 - coordinate[1]][coordinate[0]]

    def __repr__(self) -> str:
        return '\n'.join((''.join((str(v) for v in row)) for row in self.elevations))

    def __iter__(self) -> Iterator[tuple[int, int]]:
        for j in range(self.end_of_j):
            for i in range(self.end_of_i):
                yield i, j

    def __contains__(self, coordinate: tuple[int, int]) -> bool:
        return 0 <= coordinate[0] < self.end_of_i and 0 <= coordinate[1] < self.end_of_j

    @property
    def trailheads(self) -> Iterator[tuple[int, int]]:
        return (c for c in self if self[c] == 0)

    def neighbors(self, coordinate: tuple[int, int]) -> Iterator[tuple[int, int]]:
        return (neighbor for neighbor in neighbors(coordinate) if neighbor in self)

    def paths_to_summit(
            self, trailhead: tuple[int, int]
    ) -> list[list[tuple[int, int]]]:
        def dfs(
                paths: list[list[tuple[int, int]]],
                path: list[tuple[int, int]]
        ) -> list[list[tuple[int, int]]]:
            current_position = path[-1]
            # positions_visited.add(current_position)
            if self[current_position] == 9:
                paths.append(path)
            else:
                for neighbor in self.neighbors(current_position):
                    # if neighbor in positions_visited:
                    #     continue
                    if self[neighbor] - self[current_position] == 1:
                        paths = dfs(paths, path + [neighbor])
            return paths

        # positions_visited = set()

        return dfs([], [trailhead])

    def number_of_summits(self, trailhead: tuple[int, int]) -> int:
        return len({path[-1] for path in self.paths_to_summit(trailhead)})

    def score(self):
        return sum(self.number_of_summits(trailhead) for trailhead in self.trailheads)

    def rating(self):
        paths_to_summit = (self.paths_to_summit(th) for th in self.trailheads)
        return sum((len(paths) for paths in paths_to_summit))


example = Topology.from_file('example.txt')
topology = Topology.from_file('input.txt')


class MyTestCase(unittest.TestCase):
    def test_trailheads(self):
        self.assertEqual(
            [(1, 0), (0, 1), (6, 1), (2, 2), (5, 2), (6, 3), (4, 5), (2, 7), (4, 7)],
            list(example.trailheads))

    def test_paths_to_summit(self):
        self.assertEqual(5, example.number_of_summits((2, 7)))
        self.assertEqual(6, example.number_of_summits((4, 7)))
        self.assertEqual(5, example.number_of_summits((4, 5)))
        self.assertEqual(3, example.number_of_summits((7, 3)))
        self.assertEqual(1, example.number_of_summits((2, 2)))
        self.assertEqual(3, example.number_of_summits((5, 2)))
        self.assertEqual(5, example.number_of_summits((0, 1)))
        self.assertEqual(3, example.number_of_summits((6, 1)))
        self.assertEqual(5, example.number_of_summits((1, 0)))

    def test_part1(self):
        self.assertEqual(36, example.score())
        self.assertEqual(552, topology.score())

    def test_part2(self):
        self.assertEqual(81, example.rating())
        self.assertEqual(1225, topology.rating())
