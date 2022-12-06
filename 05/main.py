import unittest
import re


class TodaysTests(unittest.TestCase):
    def test_build_stack(self):
        input = ['    [D]    ',
                 '[N] [C]    ',
                 '[Z] [M] [P]',
                 ' 1   2   3 ']
        expected = {'1': ['Z', 'N'],
                    '2': ['M', 'C', 'D'],
                    '3': ['P']}
        self.assertEqual(build_stack_from_opening_lines(input), expected)
        
        instructions = ['move 1 from 2 to 1',
                        'move 3 from 1 to 3',
                        'move 2 from 2 to 1',
                        'move 1 from 1 to 2']
        final = {'1': ['C'],
                 '2': ['M'],
                 '3': ['P', 'D', 'N', 'Z']}
        rearrange_stacks(expected, instructions)
        self.assertEqual(final, expected)


def build_stack_from_opening_lines(lines: [str]):
    lines.reverse()
    if not lines[0]:
        del lines[0]
    
    # get the position from the bottom line
    stack_position = {}
    stacks = {}
    for match in re.finditer(r'\b\w+\b', lines[0]):
        stack_position[match.start()] = match[0]
        stacks[match[0]] = []
    del lines[0]
    
    for line in lines:
        line = line.replace('[', ' ').replace(']', ' ')
        for match in re.finditer(r'\b\w+\b', line):
            stack_name = stack_position[match.start()]
            stacks[stack_name].append(match[0])
    
    return stacks


def move_stacks_by_instruction(filename="input.txt"):
    opening_file_lines = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip('\n')
            if line == "":
                break
            opening_file_lines.append(line)
        
        movement_lines = [line.strip() for line in file]
    
    stacks = build_stack_from_opening_lines(opening_file_lines)
    
    rearrange_stacks(stacks, movement_lines)
    print(stacks)
    print(''.join(stack[-1] for stack in stacks.values()))
    

def rearrange_stacks(stacks: dict, movement_lines: [str]):
    for line in movement_lines:
        match = re.search(r'(\d+) from (\w+) to (\w+)', line)
        amount, from_stack, to_stack = match.groups()
        amount = int(amount)
        
        moving_stack = stacks[from_stack][-amount:]
        del stacks[from_stack][-amount:]
        # moving_stack.reverse()
        stacks[to_stack].extend(moving_stack)


if __name__ == '__main__':
    move_stacks_by_instruction()
