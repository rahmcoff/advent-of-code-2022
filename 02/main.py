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


alt_code = {'X': -1, 'Y': 0, 'Z': 1}

def alternate_rules(input) -> int:
  total = 0
  for line in input:
    line = line.strip()
    them, us = line.split(' ')
    them = them_code[them]
    us = alt_code[us]

    score = them + us
    if score == 0:
      score = 3
    if score == 4:
      score = 1

    total += score
    total += 3 * (us + 1)

  return total

class TestToday(unittest.TestCase):
  test_input = ['A Y', 'B X\n', 'C Z']

  def test_total(self):
    self.assertEqual(total_score(self.test_input), 15)

  def test_alt(self):
    self.assertEqual(alternate_rules(self.test_input), 12)


if __name__ == '__main__':
  with open('./input.txt', 'r') as f:
    code = [line for line in f]
  print(total_score(code))
  print(alternate_rules(code))
