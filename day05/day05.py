import re
from functools import cmp_to_key


def correct(rules: list[list[int]], update: list[int]) -> bool:
    for page1, page2 in rules:
        if page1 in update and page2 in update:
            if update.index(page1) > update.index(page2):
                return False
    return True


def middle(page: list[int]) -> int:
    return page[len(page) // 2]


def part1(rules: list[list[int]], updates: list[list[int]]) -> int:
    return sum([middle(update) for update in updates if correct(rules, update)])


def part2(rules: list[list[int]], updates: list[list[int]]) -> int:
    def compare(page1: int, page2: int) -> int:
        for rule in rules:
            if page1 in rule and page2 in rule:
                return -1 if rule.index(page1) < rule.index(page2) else 1
        return 0

    bad_updates = [update for update in updates if not correct(rules, update)]
    sorted_updates = [sorted(u, key=cmp_to_key(compare)) for u in bad_updates]
    return sum([middle(update) for update in sorted_updates])


def main(input_file: str) -> None:
    def paragraphs() -> list[list[str]]:
        def lines(text: str) -> list[str]:
            return [line.strip() for line in text.split('\n')]

        with (open(input_file, 'r') as file):
            return [lines(text) for text in file.read().strip().split('\n\n')]

    def to_integer_lists(lines: list[str]) -> list[list[int]]:
        return [[int(i) for i in m] for m in (re.findall(r'\d+', l) for l in lines)]

    rules, updates = map(to_integer_lists, paragraphs())

    print(input_file)
    print('    part1: ', part1(rules, updates))
    print('    part2: ', part2(rules, updates))


main('example.txt')
main('input.txt')
