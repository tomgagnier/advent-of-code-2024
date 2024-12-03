import operator
import re
from functools import reduce


def multiply(multiply_token: str) -> int:
    operands = map(int, re.findall('\d+', multiply_token))
    return reduce(operator.mul, operands)


def sum_products(multiply_tokens):
    return sum(map(multiply, multiply_tokens))


def part1(expression: str) -> int:
    multiply_tokens = re.findall(r'mul\(\d+,\d+\)', expression)
    return sum_products(multiply_tokens)


def part2(expression: str) -> int:
    skip = False
    qualified_multiply_tokens = []
    tokens = re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", expression)
    for token in tokens:
        if token == "don't()":
            skip = True
        elif token == "do()":
            skip = False
        elif not skip:
            qualified_multiply_tokens.append(token)
    return sum_products(qualified_multiply_tokens)


def main(input_file: str) -> None:
    with open(input_file, 'r') as file:
        expression = ''.join((line.strip() for line in file.readlines()))

    print(input_file)
    print('    part1: ', part1(expression))
    print('    part2: ', part2(expression))


main('example.txt')
main('input.txt')
