import utilities.unittest


def split_if_even_length(i: int) -> tuple[int, int] | None:
    s = f'{i}'
    l = len(s)
    if l % 2 == 0:
        middle = l // 2
        return int(s[0:middle]), int(s[middle:])


def count_descendants(stones: list[int], number_of_blinks: int) -> int:
    def count_descendents_for_one(stone: int, remaining: int) -> int:
        if (stone, remaining) in memo:
            return memo[(stone, remaining)]
        if remaining == 0:
            result = 1
        elif stone == 0:
            result = count_descendents_for_one(1, remaining - 1)
        elif split := split_if_even_length(stone):
            result = (
                    count_descendents_for_one(split[0], remaining - 1) +
                    count_descendents_for_one(split[1], remaining - 1)
            )
        else:
            result = count_descendents_for_one(2024 * stone, remaining - 1)

        memo[(stone, remaining)] = result

        return result

    memo = {}

    return sum(count_descendents_for_one(stone, number_of_blinks) for stone in stones)


STONES = [28, 4, 3179, 96938, 0, 6617406, 490, 816207]


class TestDay11(utilities.unittest.TimedTestCase):

    def test_example_25(self):
        assert 55312 == count_descendants([125, 17], 25)

    def test_example_75(self):
        assert 65601038650482 == count_descendants([125, 17], 75)

    def test_part1(self):
        assert 189167 == count_descendants(STONES, 25)

    def test_part2(self):
        assert 225253278506288 == count_descendants(STONES, 75)
