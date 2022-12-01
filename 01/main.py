import unittest
from io import StringIO


def most_calories(input_file, number_to_return=1) -> ([(int, int)], int):
    """
    Returns the top number_to_return elves and their calorie counts, along with the total calorie count
    """
    elves: [int] = [0]
    current_elf = 0

    for line in input_file:
        line = line.strip()
        if line == '':
            current_elf += 1
            elves.append(0)
            continue
        elves[current_elf] += int(line)

    most = elves.copy()
    most.sort(reverse=True)

    return_values = []
    total_cal = 0
    for i in range(number_to_return):
        ret_line = elves.index(most[i])+1, most[i]
        return_values.append(ret_line)
        total_cal += most[i]
    return return_values, total_cal


class TestToday(unittest.TestCase):
    test_input = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

    def test_most_calories(self):
        self.assertEqual(([(4, 24000)], 24000), most_calories(StringIO(self.test_input)))

    def test_top_three(self):
        expected = [(4, 24000), (3, 11000), (5, 10000)], 45000
        self.assertEqual(expected, most_calories(StringIO(self.test_input), 3))


if __name__ == '__main__':
    with open('./input.txt', 'r') as file:
        elf, calories = most_calories(file)

    print(f"The top {len(elf)} elves are carrying a total of {calories} kcal\n")

    with open('./input.txt', 'r') as file:
        elf, calories = most_calories(file, 3)

    print(f"The top {len(elf)} elves are carrying a total of {calories} kcal\n")
