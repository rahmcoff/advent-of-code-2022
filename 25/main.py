import unittest
from math import log, ceil


def snafu(number: str) -> int:
    value = 0
    exp = 1
    for digit in reversed(number):
        if digit == '-':
            value -= 1 * exp
        elif digit == '=':
            value -= 2 * exp
        else:
            value += int(digit) * exp
        exp *= 5
    return value


def ufans(number: int) -> str:
    digits = [0]
    while number > 0:
        digit = number % 5
        if digit + digits[-1] > 2:
            digits[-1] += digit - 5
            digits.append(1)
        else:
            digits[-1] += digit
            digits.append(0)
        number //= 5
        
    if digits[-1] == 0:
        digits.pop()
        
    for place, digit in enumerate(digits):
        if digit >= 0:
            digits[place] = str(digit)
        elif digit == -2:
            digits[place] = '='
        else:
            digits[place] = '-'
    return ''.join(reversed(digits))


class TodayTest(unittest.TestCase):
    def test_part_1(self):
        self.assertEqual(snafu('1=-0-2'), 1747)
        self.assertEqual(snafu('12111'), 906)
        self.assertEqual(snafu('2=0='), 198)
        self.assertEqual(snafu('21'), 11)
        self.assertEqual(snafu('2=01'), 201)
        self.assertEqual(snafu('111'), 31)
        self.assertEqual(snafu('20012'), 1257)
        self.assertEqual(snafu('112'), 32)
        self.assertEqual(snafu('1=-1='), 353)
        self.assertEqual(snafu('1-12'), 107)
        self.assertEqual(snafu('12'), 7)
        self.assertEqual(snafu('1='), 3)
        self.assertEqual(snafu('122'), 37)
        
    def test_part_1_reverse(self):
        self.assertEqual('1=-0-2', ufans(1747))
        self.assertEqual('12111', ufans(906))
        self.assertEqual('2=0=', ufans(198))
        self.assertEqual('21', ufans(11))
        self.assertEqual('2=01', ufans(201))
        self.assertEqual('111', ufans(31))
        self.assertEqual('20012', ufans(1257))
        self.assertEqual('112', ufans(32))
        self.assertEqual('1=-1=', ufans(353))
        self.assertEqual('1-12', ufans(107))
        self.assertEqual('12', ufans(7))
        self.assertEqual('1=', ufans(3))
        self.assertEqual('122', ufans(37))


if __name__ == '__main__':
    with open('input.txt') as f:
        fuel = sum(snafu(line.strip()) for line in f)
    print(ufans(fuel))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
