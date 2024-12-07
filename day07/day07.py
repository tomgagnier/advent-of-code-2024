import re
from dataclasses import dataclass
from functools import reduce
from itertools import product
from typing import Callable


def evaluate(operands: list[int], *operators: Callable[[int, int], int]) -> int:
    return reduce(lambda acc, i: operators[i](acc, operands[i + 1]),
                  range(len(operators)), operands[0])


@dataclass(frozen=True)
class Equation:
    expected_value: int
    operands: list[int]

    def evaluate(self, *operators: Callable[[int, int], int]) -> int:
        return reduce(lambda acc, i: operators[i](acc, self.operands[i + 1]),
                      range(len(operators)),
                      self.operands[0])

    def test(self, *operators: Callable[[int, int], int]):
        return self.expected_value == self.evaluate(*operators)

    def valid(self, *operators: Callable[[int, int], int]) -> bool:
        operations = product(operators, repeat=(len(self.operands) - 1))
        return any(self.test(*operation) for operation in operations)


def main(input_file: str) -> None:
    with (open(input_file, 'r') as file):
        matches = (re.findall(r'\d+', l) for l in file.readlines())
        integers = ([int(i) for i in m] for m in matches)
        equations = [Equation(v[0], v[1:]) for v in integers]

    def sum_of_valid_equations(*operators: Callable[[int, int], int]) -> int:
        return sum(eqn.expected_value for eqn in equations if eqn.valid(*operators))

    add = lambda a, b: a + b
    multiply = lambda a, b: a * b
    concatenate = lambda a, b: int(f'{a}{b}')

    print(input_file)
    print('    part1: ', sum_of_valid_equations(add, multiply))
    print('    part2: ', sum_of_valid_equations(add, multiply, concatenate))


main('example.txt')
main('input.txt')
