import unittest

them_code = {'A': 1, 'B': 2, 'C': 3}
us_code = {'X': 1, 'Y': 2, 'Z': 3}


def total_score(input: [str]) -> int:
  score = 0
  for line in input:
    line = line.strip()
    them, us = line.split(' ')
    score += single_game_score(them, us)
  return score


def single_game_score(them: str, us: str) -> int:
  them = them_code[them]
  us = us_code[us]

  score = us
  if us == them:
    return score + 3
  diff = us - them
  if diff in (1, -2):
    score += 6
  return score


class TestToday(unittest.TestCase):

  def test_total(self):
    test_input = ['A Y', 'B X\n', 'C Z']
    self.assertEqual(total_score(test_input), 15)


if __name__ == '__main__':
  with open('./input.txt', 'r') as f:
    code = [line for line in f]
  print(total_score(code))
