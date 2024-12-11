import re
from dataclasses import dataclass
from itertools import repeat
from typing import Self, Callable
from unittest import TestCase


@dataclass
class Disk:
    ids: list[int]

    def __repr__(self):
        return self.ids_to_str(self.ids)

    @staticmethod
    def ids_to_str(ids):
        return ''.join(map(lambda i: str(i) if i >= 0 else '.', ids))

    def tuple_to_str(self, r: range) -> str:
        return self.ids_to_str([self[i] for i in r if i in range(len(self.ids))])

    def __getitem__(self, i: int) -> int:
        return self.ids[i]

    def __setitem__(self, i: int, v: int):
        self.ids[i] = v

    @classmethod
    def from_file(cls, input_file: str) -> Self:
        with (open(input_file, 'r') as file):
            sizes = [int(i) for i in re.findall(r'\d', file.readlines()[0])]
        block_ids = []
        for i, size in enumerate(sizes):
            block_ids += repeat(i // 2 if i % 2 == 0 else -1, size)
        return Disk(block_ids)

    def find(self, start: int, predicate: Callable[[int], bool]) -> int | None:
        return next((i for i in range(start, len(self.ids), 1) if predicate(i)), None)

    @staticmethod
    def reverse_find(start: int, predicate: Callable[[int], bool]) -> int | None:
        return next((i for i in range(start, -1, -1) if predicate(i)), None)

    def first_free_block(self, start: int) -> int | None:
        return self.find(start, lambda i: self[i] < 0)

    def first_used_block(self, start: int) -> int | None:
        return self.find(start, lambda i: self[i] >= 0)

    def last_used_block(self, start: int) -> int | None:
        return self.reverse_find(start, lambda i: self[i] >= 0)

    def part1(self) -> Self:
        free = self.first_free_block(0)
        last = self.last_used_block(len(self.ids) - 1)
        while free < last:
            self[free] = self[last]
            self.ids[last] = -1
            free = self.first_free_block(free)
            last = self.last_used_block(last)
        return self

    def first_free_range(self, start: int) -> range | None:
        if begin := self.first_free_block(start):
            if end := self.first_used_block(begin):
                return range(begin, end)
        return None

    def last_used_range(self, start: int) -> range | None:
        if end := self.last_used_block(start):
            if begin := self.reverse_find(end, lambda i: self[i] != self[end]):
                return range(begin + 1, end + 1)
        return None

    def copy(self, source, target) -> int:
        for s, t in zip(list(source), list(target)):
            self[t] = self[s]
            self[s] = -1
        return target.stop + 1

    def part2(self) -> Self:
        end = len(self.ids) - 1
        while used_range := self.last_used_range(end):
            begin = 0
            while free_range := self.first_free_range(begin):
                if free_range.stop > used_range.start:
                    break
                if len(free_range) >= len(used_range):
                    self.copy(used_range, free_range)
                    break
                begin = free_range.stop
            end = used_range.start - 1

        return self

    def checksum(self) -> int:
        return sum([i * ID for i, ID in enumerate(self.ids) if ID >= 0])

class Test(TestCase):

    def setUp(self):
        self.example = Disk.from_file('example.txt')

    def test_part1(self):
        self.assertEqual(1928, self.example.part1().checksum())

    def test_part2(self):
        self.assertEqual(2858, self.example.part2().checksum())

input_file = 'input.txt'
print('part1 ', Disk.from_file(input_file).part1().checksum())
print('part2 ', Disk.from_file(input_file).part2().checksum())
