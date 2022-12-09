import unittest


class TodayTest(unittest.TestCase):
    sample = ['R 4',
              'U 4',
              'L 3',
              'D 1',
              'R 4',
              'D 1',
              'L 5',
              'R 2']
    
    def test_tail_path(self):
        self.assertEqual(count_tail_path(self.sample), 13)
    
    longer_sample = ['R 5',
                     'U 8',
                     'L 8',
                     'D 3',
                     'R 17',
                     'D 10',
                     'L 25',
                     'U 20']
    
    def test_long_rope(self):
        self.assertEqual(count_tail_path(self.sample, 10), 1)
        self.assertEqual(count_tail_path(self.longer_sample, 10), 36)


def count_tail_path(instructions: [str], length=2) -> int:
    rope_segments = [[0, 0] for i in range(length)]
    head_pos = rope_segments[0]
    tail_pos = rope_segments[length - 1]
    tail_visited = {f"{tail_pos[0]},{tail_pos[1]}"}
    
    for step in instructions:
        direction = step[0]
        count = int(step[2:])
        
        for i in range(count):
            if direction == 'U':
                head_pos[1] += 1
            elif direction == 'D':
                head_pos[1] -= 1
            elif direction == 'L':
                head_pos[0] -= 1
            elif direction == 'R':
                head_pos[0] += 1
            
            for seg in range(1, length):
                if abs(rope_segments[seg - 1][0] - rope_segments[seg][0]) <= 1 and \
                      abs(rope_segments[seg - 1][1] - rope_segments[seg][1]) <= 1:
                    break
                # move the tail
                if rope_segments[seg - 1][0] > rope_segments[seg][0]:
                    rope_segments[seg][0] += 1
                elif rope_segments[seg - 1][0] < rope_segments[seg][0]:
                    rope_segments[seg][0] -= 1
                if rope_segments[seg - 1][1] > rope_segments[seg][1]:
                    rope_segments[seg][1] += 1
                elif rope_segments[seg - 1][1] < rope_segments[seg][1]:
                    rope_segments[seg][1] -= 1
            
            tail_visited.add(f"{tail_pos[0]},{tail_pos[1]}")
    
    return len(tail_visited)


if __name__ == '__main__':
    with open('input.txt') as f:
        instructions = [l.strip() for l in f]
    
    print(count_tail_path(instructions))
    print(count_tail_path(instructions, 10))
