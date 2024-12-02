import re


def safe(report: list[int]) -> bool:
    indexes = range(len(report) - 1)
    ascending = all(report[i] < report[i + 1] for i in indexes)
    descending = all(report[i] > report[i + 1] for i in indexes)
    if ascending or descending:
        max_level_delta = 3
        return all(abs(report[i] - report[i + 1]) <= max_level_delta for i in indexes)
    return False


def safe_or_damped(report: list[int]) -> bool:
    damped_reports = (report[:i] + report[i + 1:] for i in range(len(report)))
    return safe(report) or any(safe(r) for r in damped_reports)


def main(input_file: str):
    with open(input_file, 'r') as file:
        matches = (re.findall(r'\d+', line) for line in file)
        reports = [[int(level) for level in match] for match in matches]

    print(input_file)
    print('    part1: ', sum(1 for report in reports if safe(report)))
    print('    part2: ', sum(1 for report in reports if safe_or_damped(report)))


main('example.txt')
main('input.txt')
