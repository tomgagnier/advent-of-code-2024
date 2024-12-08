import re

def main(input_file: str) -> None:
    print(input_file)
    with (open(input_file, 'r') as file):
        matches = (re.findall(r'\d+', l) for l in file.readlines())
        integers = ([int(i) for i in m] for m in matches)

    print('    part1: ', )
    print('    part2: ', )

main('example.txt')
# main('input.txt')
