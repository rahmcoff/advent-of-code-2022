import unittest


class TestToday(unittest.TestCase):
    test_data = ['4-71,36-72',
                 '2-4,6-8',
                 '2-3,4-5',
                 '5-7,7-9',
                 '2-8,3-7',
                 '6-6,4-6',
                 '2-6,4-8']
    
    def test_single_line(self):
        self.assertEqual(False, full_contains(self.test_data[0]), self.test_data[0])
        self.assertEqual(False, full_contains(self.test_data[1]), self.test_data[1])
        self.assertEqual(False, full_contains(self.test_data[2]), self.test_data[2])
        self.assertEqual(False, full_contains(self.test_data[3]), self.test_data[3])
        self.assertEqual(True, full_contains(self.test_data[4]), self.test_data[4])
        self.assertEqual(True, full_contains(self.test_data[5]), self.test_data[5])
        self.assertEqual(False, full_contains(self.test_data[6]), self.test_data[6])
    
    def test_all_lines(self):
        self.assertEqual(2, count_contains(self.test_data))

    def test_overlap(self):
        self.assertEqual(True, overlaps(self.test_data[0]), self.test_data[0])
        self.assertEqual(False, overlaps(self.test_data[1]), self.test_data[1])
        self.assertEqual(False, overlaps(self.test_data[2]), self.test_data[2])
        self.assertEqual(True, overlaps(self.test_data[3]), self.test_data[3])
        self.assertEqual(True, overlaps(self.test_data[4]), self.test_data[4])
        self.assertEqual(True, overlaps(self.test_data[5]), self.test_data[5])
        self.assertEqual(True, overlaps(self.test_data[6]), self.test_data[6])


def full_contains(line: str) -> bool:
    elves = [[int(n) for n in e.split('-')] for e in line.split(',')]
    if (elves[0][0] >= elves[1][0] and elves[0][1] <= elves[1][1]) \
          or (elves[0][0] <= elves[1][0] and elves[0][1] >= elves[1][1]):
        return True
    return False


def count_contains(lines: [str]) -> int:
    matching = [l for l in lines if full_contains(l)]
    # for l in matching:
    #     print(l)
    return len(matching)


def overlaps(line: str) -> bool:
    elves = [[int(n) for n in e.split('-')] for e in line.split(',')]
    if elves[0][0] <= elves[1][1] and elves[0][1] >= elves[1][0]:
        return True
    return False


def count_overlaps(lines: [str]) -> int:
    matching = [l for l in lines if overlaps(l)]
    # for l in matching:
    #     print(l)
    return len(matching)


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = [l.strip() for l in f]
    print(count_contains(lines))
    print(count_overlaps(lines))
