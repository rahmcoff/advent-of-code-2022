import unittest
import re


class TestToday(unittest.TestCase):
    def test_part_1(self):
        test_calc = MonkeyCalc()
        test_calc.load_file('test_input.txt')
        test_calc.solve()
        self.assertEqual(152, test_calc['root'])
        
    def test_part_2(self):
        test_calc = MonkeyCalc()
        test_calc.load_file('test_input.txt')
        test_calc.solve_unsolve()
        self.assertEqual(301, test_calc['humn'])
        self.assertEqual(150, test_calc['root'])


class MonkeyCalc:
    solved_monkeys: dict[str, int]
    unsolved_monkeys: dict[str, tuple[str, str, str]]
    
    def load_file(self, filename):
        self.solved_monkeys = {}
        self.unsolved_monkeys = {}
        
        problem_monkey = re.compile(r'(\w+): (\w+) (.) (\w+)')
        number_monkey = re.compile(r'(\w+): (\d+)')
        with open(filename) as f:
            for line in f:
                match = problem_monkey.match(line)
                if match:
                    self.unsolved_monkeys[match[1]] = match[2], match[4], match[3]
                else:
                    match = number_monkey.match(line)
                    self.solved_monkeys[match[1]] = int(match[2])
    
    def solve(self):
        while self.unsolved_monkeys:
            solved_names = []
            for name, (left, right, op) in self.unsolved_monkeys.items():
                if left not in self.solved_monkeys or right not in self.solved_monkeys:
                    continue
                
                if op == '+':
                    self.solved_monkeys[name] = self.solved_monkeys[left] + self.solved_monkeys[right]
                elif op == '-':
                    self.solved_monkeys[name] = self.solved_monkeys[left] - self.solved_monkeys[right]
                elif op == '*':
                    self.solved_monkeys[name] = self.solved_monkeys[left] * self.solved_monkeys[right]
                elif op == '/':
                    self.solved_monkeys[name] = self.solved_monkeys[left] // self.solved_monkeys[right]
                solved_names.append(name)
                
            for name in solved_names:
                del self.unsolved_monkeys[name]
                
    def solve_unsolve(self):
        del self.solved_monkeys['humn']
        humn_dependent: dict[str, tuple[str, str, str]] = {'humn': ('', '', '')}
        
        while self.unsolved_monkeys:
            solved_names = []
            for name, (left, right, op) in self.unsolved_monkeys.items():
                if left in humn_dependent and right in humn_dependent:
                    print(f"!!! {name} = {left} {op} {right} !!!")
                if left in humn_dependent or right in humn_dependent:
                    humn_dependent[name] = left, right, op
                    solved_names.append(name)
                    continue

                if left not in self.solved_monkeys or right not in self.solved_monkeys:
                    continue
        
                if op == '+':
                    self.solved_monkeys[name] = self.solved_monkeys[left] + self.solved_monkeys[right]
                elif op == '-':
                    self.solved_monkeys[name] = self.solved_monkeys[left] - self.solved_monkeys[right]
                elif op == '*':
                    self.solved_monkeys[name] = self.solved_monkeys[left] * self.solved_monkeys[right]
                elif op == '/':
                    self.solved_monkeys[name] = self.solved_monkeys[left] // self.solved_monkeys[right]
                solved_names.append(name)
    
            for name in solved_names:
                del self.unsolved_monkeys[name]
                
        left, right, _ = humn_dependent['root']
        if left in self.solved_monkeys:
            value = self.solved_monkeys[right] = self.solved_monkeys[left]
            next_monkey = right
        else:
            value = self.solved_monkeys[left] = self.solved_monkeys[right]
            next_monkey = left
        self.solved_monkeys['root'] = value

        while next_monkey != 'humn':
            left, right, op = humn_dependent[next_monkey]
            if op == '+':
                next_monkey, solved = (left, right) if right in self.solved_monkeys else (right, left)
                value = self.solved_monkeys[next_monkey] = value - self.solved_monkeys[solved]
            elif op == '-' and left in self.solved_monkeys:
                next_monkey = right
                value = self.solved_monkeys[next_monkey] = self.solved_monkeys[left] - value
            elif op == '-' and right in self.solved_monkeys:
                next_monkey = left
                value = self.solved_monkeys[next_monkey] = self.solved_monkeys[right] + value
            elif op == '*':
                next_monkey, solved = (left, right) if right in self.solved_monkeys else (right, left)
                value = self.solved_monkeys[next_monkey] = value // self.solved_monkeys[solved]
            elif op == '/' and left in self.solved_monkeys:
                next_monkey = right
                value = self.solved_monkeys[next_monkey] = self.solved_monkeys[left] // value
            elif op == '/' and right in self.solved_monkeys:
                next_monkey = left
                value = self.solved_monkeys[next_monkey] = self.solved_monkeys[right] * value

    def __getitem__(self, item):
        return self.solved_monkeys[item]


if __name__ == '__main__':
    calc = MonkeyCalc()
    calc.load_file('input.txt')
    calc.solve()
    print(calc['root'])
    
    calc.load_file('input.txt')
    calc.solve_unsolve()
    print(calc['humn'])
