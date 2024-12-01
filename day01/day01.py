import re

from sortedcollections import SortedList

list0 = SortedList()
list1 = SortedList()

with open('input.txt', 'r') as file:
    for line in file:
        matches = re.findall(r'\d+', line)
        list0.add(int(matches[0]))
        list1.add(int(matches[1]))

indexes = range(len(list0))

print('part1:', sum(map(lambda i: abs(list0[i] - list1[i]), indexes)))
print('part2:', sum(map(lambda i: list1.count(list0[i]) * list0[i], indexes)))
