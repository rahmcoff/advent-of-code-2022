import unittest


class TestToday(unittest.TestCase):
    test_data = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw""".split('\n')

    def test_single_line(self):
        self.assertEqual(line_priority(self.test_data[0]), 16)
        self.assertEqual(line_priority(self.test_data[1]), 38)
        self.assertEqual(line_priority(self.test_data[2]), 42)
        self.assertEqual(line_priority(self.test_data[3]), 22)
        self.assertEqual(line_priority(self.test_data[4]), 20)
        self.assertEqual(line_priority(self.test_data[5]), 19)

    def test_sum_priority(self):
        self.assertEqual(backpack_priority(self.test_data), 157)

    def test_badge_in_backpacks(self):
        self.assertEqual(18, common_badge(self.test_data[0:3]))
        self.assertEqual(52, common_badge(self.test_data[3:6]))

    def test_all_common_badges(self):
        self.assertEqual(70, all_common_badges(self.test_data))


def backpack_priority(input: [str]) -> int:
    return sum(line_priority(line) for line in input)


def line_priority(input: str) -> int:
    split = len(input) // 2
    first_half = input[:split]
    second_half = input[split:]

    in_both = None
    for letter in first_half:
        if letter in second_half:
            return get_value(letter)


def get_value(letter: str) -> int:
    in_both = ord(letter)
    if in_both <= ord('Z'):
        return in_both - ord('A') + 27
    return in_both - ord('a') + 1


def common_badge(input: [str]) -> int:
    for letter in input[0]:
        if letter in input[1] and letter in input[2]:
            return get_value(letter)


def all_common_badges(input: [str]) -> int:
    priority_sum = 0
    for i in range(0, len(input), 3):
        priority_sum += common_badge(input[i:i+3])
    return priority_sum


if __name__ == '__main__':
    with open('./input.txt', 'r') as f:
        rows = [line.strip() for line in f]

    print(backpack_priority(rows))
    print(all_common_badges(rows))
