def horizontal(lines: list[str]) -> list[str]:
    return lines.copy() + list(map(lambda l: l[::-1], lines))


def vertical(lines: list[str]) -> list[str]:
    verticals = []
    for i in range(len(lines)):
        top_to_bottom = ''
        for j in range(len(lines[0])):
            top_to_bottom += lines[j][i]
        verticals.append(top_to_bottom)
        verticals.append(top_to_bottom[::-1])
    return verticals


def diagonal(lines: list[str]) -> list[str]:
    diagonals = []
    for d in range(len(lines) + len(lines[0]) - 1):
        left_to_right = ''
        right_to_left = ''
        for i in range(max(0, d - len(lines[0]) + 1), min(len(lines), d + 1)):
            left_to_right += lines[i][d - i]
            right_to_left += lines[i][len(lines[0]) - 1 - d + i]
        diagonals.append(left_to_right)
        diagonals.append(left_to_right[::-1])
        diagonals.append(right_to_left)
        diagonals.append(right_to_left[::-1])
    return diagonals


def part1(lines: list[str]) -> int:
    return sum(
        candidate.count('XMAS')
        for candidate
        in horizontal(lines) + vertical(lines) + diagonal(lines)
    )


def part2(lines: list[str]) -> int:
    def mas(candidate: str) -> bool:
        return candidate == 'MAS' or candidate == 'SAM'

    count = 0
    for i in range(1, len(lines) - 1):
        for j in range(1, len(lines[0]) - 1):
            sw_to_ne = lines[i - 1][j - 1] + lines[i][j] + lines[i + 1][j + 1]
            nw_to_se = lines[i - 1][j + 1] + lines[i][j] + lines[i + 1][j - 1]
            if mas(sw_to_ne) and mas(nw_to_se):
                count += 1
    return count


def main(input_file: str) -> None:
    with open(input_file, 'r') as file:
        lines = [line.strip() for line in file.readlines()]

    print(input_file)
    print('    part1: ', part1(lines))
    print('    part2: ', part2(lines))

main('input.txt')
