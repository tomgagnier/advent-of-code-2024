from typing import Any, Iterator


class Lab:
    def __init__(self, lines: list[str]):
        self.elements = [list(line.strip()) for line in lines]
        self.max_i = len(self.elements[0])
        self.max_j = len(self.elements)
        self.guard = next(((i, j) for i, j in self if self[i, j] in '<>^v'))

    def __getitem__(self, coordinates: tuple[int, int]) -> Any:
        return self.elements[self.max_j - 1 - coordinates[1]][coordinates[0]]

    def __repr__(self) -> str:
        return '\n'.join([''.join(self.elements[j]) for j in range(self.max_j)])

    def __iter__(self) -> Iterator[tuple[int, int]]:
        for j in range(self.max_j):
            for i in range(self.max_i):
                yield i, j

    def __contains__(self, coordinates: tuple[int, int]) -> bool:
        return 0 <= coordinates[0] < self.max_i and 0 <= coordinates[1] < self.max_j


def add(v0: tuple[int, int], v1: tuple[int, int]) -> tuple[int, int]:
    return v0[0] + v1[0], v0[1] + v1[1]


STRAIGHT_MOVE = {'<': (-1, 0), '>': (1, 0), '^': (0, 1), 'v': (0, -1)}
RIGHT_TURN = {'<': '^', '^': '>', '>': 'v', 'v': '<'}


def move_guard(
        lab: Lab, obstacle: tuple[int, int] | None = None
) -> tuple[str, dict[tuple[int, int], str]]:
    guard_position = lab.guard
    guard_direction = lab[guard_position]
    steps = {guard_position: guard_direction}
    while True:
        if guard_position in steps:
            steps[guard_position] += guard_direction
        else:
            steps[guard_position] = guard_direction
        next_position = add(guard_position, STRAIGHT_MOVE[guard_direction])
        if next_position not in lab:
            return 'gone', steps
        if guard_direction in steps.get(next_position, ''):
            return 'loop', steps
        if lab[next_position] == '#' or next_position == obstacle:
            guard_direction = RIGHT_TURN[guard_direction]
        else:
            guard_position = next_position


def main(input_file: str) -> None:
    with open(input_file, 'r') as file:
        lab = Lab(file.readlines())

    _, steps = move_guard(lab)
    loop_count = sum(
        [1 for obstacle in steps if move_guard(lab, obstacle)[0] == 'loop'])

    print(input_file)
    print('    part1: ', len(steps))
    print('    part2: ', loop_count)


main('example.txt')
main('input.txt')
