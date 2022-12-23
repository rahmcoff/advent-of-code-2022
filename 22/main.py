import unittest
import re


class TodayTest(unittest.TestCase):
    def test_part_1(self):
        test_path = PathFinder()
        test_path.load_file('test_input.txt')
        test_path.follow_path()
        test_path.print_map()
        self.assertEqual(6, test_path.row)
        self.assertEqual(8, test_path.col)
        self.assertEqual('>', test_path.dir)
        self.assertEqual(6032, test_path.password)
        
    def test_part_2(self):
        test_path = PathFinder()
        test_path.load_file('test_input.txt')
        test_path.cube = True
        test_path.follow_path()
        test_path.print_map()
        self.assertEqual(5, test_path.row)
        self.assertEqual(7, test_path.col)
        self.assertEqual('^', test_path.dir)
        self.assertEqual(5031, test_path.password)
        
    def test_big_cube(self):
        path = PathFinder()
        path.load_file('input.txt')
        path.cube = True
        
        path.row = 2
        path.directions = [(1, 'L'), (2, 'R'), (2, 'R'), (4, 'R'), (5, 'R'), (1, 'R'), (2, '')]
        path.follow_path()
        self.assertEqual('>', path.dir)

        path.row = 6
        path.col = 150
        path.directions = [(3, 'R'), (1, 'R'), (4, '')]
        path.follow_path()
        self.assertEqual('<', path.dir)

        path.row = 56
        path.col = 51
        path.directions = [(3, 'L'), (1, 'L'), (4, '')]
        path.follow_path()
        self.assertEqual('>', path.dir)

        path.row = 58
        path.col = 100
        path.directions = [(3, 'R'), (2, 'R'), (4, '')]
        path.follow_path()
        self.assertEqual('<', path.dir)

        path.row = 101
        path.col = 99
        path.directions = [(5, 'R'), (3, 'R'), (5, '')]
        path.follow_path()
        self.assertEqual('<', path.dir)

        path.row = 103
        path.col = 1
        path.directions = [(5, 'R'), (1, 'R'), (5, '')]
        path.follow_path()
        self.assertEqual('>', path.dir)
        
        path.row = 152
        path.col = 49
        path.directions = [(5, 'R'), (1, 'R'), (5, '')]
        path.follow_path()
        self.assertEqual('<', path.dir)

        path.col = 2
        path.directions = [(5, 'R'), (1, 'R'), (5, '')]
        path.follow_path()
        self.assertEqual('>', path.dir)

        path.col = 2
        path.row = 199
        path.dir = 'v'
        path.follow_path()
        self.assertEqual('^', path.dir)
        
        path.print_map()
        
class PathFinder:
    cube = False
    
    row = 1
    col = 1
    dir = '>'
    
    map: list[dict[int, str]]
    directions: list[tuple[int, str]]
    
    def load_file(self, filename):
        self.map = [{}]
        self.directions = []
        with open(filename) as f:
            for line in f:
                line = line.strip('\r\n')
                if not line:
                    break
                
                map_line = {}
                for pos, char in enumerate(line):
                    if char != ' ':
                        map_line[pos + 1] = char
                self.map.append(map_line)
            
            last_line = f.readline().strip()
            for match in re.finditer(r'(\d+)([LR])', last_line):
                self.directions.append((int(match[1]), match[2]))
            match = re.search(r'\d+$', last_line)
            if match:
                self.directions.append((int(match[0]), ''))
                
        self.row = 1
        self.col = min(self.map[1].keys())
    
    def follow_path(self):
        for steps, turn in self.directions:
            for _ in range(steps):
                self.map[self.row][self.col] = self.dir
                next_row, next_col, next_dir = self.next_step()
                if self.map[next_row][next_col] == '#':
                    break
                self.row, self.col, self.dir = next_row, next_col, next_dir
            if (turn == 'R' and self.dir == '>') or (turn == 'L' and self.dir == '<'):
                self.dir = 'v'
            elif (turn == 'L' and self.dir == '>') or (turn == 'R' and self.dir == '<'):
                self.dir = '^'
            elif (turn == 'R' and self.dir == 'v') or (turn == 'L' and self.dir == '^'):
                self.dir = '<'
            elif (turn == 'L' and self.dir == 'v') or (turn == 'R' and self.dir == '^'):
                self.dir = '>'
    
    def next_step(self) -> tuple[int, int, str]:  # row, col, dir
        if self.dir == '>':
            row, col, dir = self.row, self.col + 1, self.dir
        elif self.dir == 'v':
            row, col, dir = self.row + 1, self.col, self.dir
        elif self.dir == '<':
            row, col, dir = self.row, self.col - 1, self.dir
        else:
            row, col, dir = self.row - 1, self.col, self.dir
            
        if row >= len(self.map) or col not in self.map[row]:
            if not self.cube:
                if self.dir == '>':
                    col = min(self.map[row].keys())
                elif self.dir == 'v':
                    row = min([r for r in range(len(self.map)) if col in self.map[r]])
                elif self.dir == '<':
                    col = max(self.map[row].keys())
                elif self.dir == '^':
                    row = max([r for r in range(len(self.map)) if col in self.map[r]])
            elif len(self.map) < 50:
                row, col, dir = self.small_cube(row, col, dir)
            else:
                row, col, dir = self.big_cube(row, col, dir)
                
        return row, col, dir

    def small_cube(self, row:int, col:int, dir:str) -> tuple[int, int, str]:
        if dir == '^':
            if col in range(1, 5):
                col = 13 - col
                row = 1
                dir = 'v'
            elif col in range(5, 9):
                row = col - 4
                col = 9
                dir = '>'
            elif col in range(9, 13):
                col = 13 - col
                row = 5
                dir = 'v'
            else:
                row = 17 - col
                col = 12
                dir = '<'
        elif dir == '>':
            if row in range(1, 5):
                row = 13 - row
                col = 16
                dir = '<'
            elif row in range(5, 9):
                col = 21 - row
                row = 9
                dir = 'v'
            else:
                row = 13 - row
                col = 12
                dir = '<'
        elif dir == 'v':
            if col in range(1, 5):
                col = 13 - col
                row = 12
                dir = '^'
            elif col in range(5, 9):
                row = 17 - col
                col = 9
                dir = '>'
            elif col in range(9, 13):
                col = 13 - col
                row = 8
                dir = '^'
            else:
                row = col - 8
                col = 1
                dir = '>'
        else:
            if row in range(1, 5):
                col = row + 4
                row = 5
                dir = 'v'
            elif row in range(5, 9):
                col = 21 - row
                row = 16
                dir = '^'
            else:
                col = 17 - row
                row = 8
                dir = '^'
        return row, col, dir
    
    def big_cube(self, row:int, col:int, dir:str) -> tuple[int, int, str]:
        if dir == '^':
            if col <= 50:
                row = col + 50
                col = 51
                dir = '>'
            elif col <= 100:
                row = col + 100
                col = 1
                dir = '>'
            else:
                col = col - 100
                row = 200
                dir = '^'
        elif dir == '>':
            if row <= 50:
                row = 151 - row
                col = 100
                dir = '<'
            elif row <= 100:
                col = row + 50
                row = 50
                dir = '^'
            elif row <= 150:
                row = 151 - row
                col = 150
                dir = '<'
            else:
                col = row - 100
                row = 150
                dir = '^'
        elif dir == 'v':
            if col <= 50:
                col = 100 + col
                row = 1
                dir = 'v'
            elif col <= 100:
                row = col + 100
                col = 50
                dir = '<'
            else:
                row = col - 50
                col = 100
                dir = '<'
        else:
            if row <= 50:
                row = 151 - row
                col = 1
                dir = '>'
            elif row <= 100:
                col = row - 50
                row = 101
                dir = 'v'
            elif row <= 150:
                row = 151 - row
                col = 51
                dir = '>'
            else:
                col = row - 100
                row = 1
                dir = 'v'
        return row, col, dir

    def print_map(self):
        for line in self.map:
            if not line:
                continue
            print(''.join(line[i] if i in line else ' ' for i in range(max(line.keys()) + 1)))
    
    @property
    def password(self):
        dir_map = {'>': 0, 'v': 1, '<': 2, '^': 3}
        return 1000 * self.row + 4 * self.col + dir_map[self.dir]


if __name__ == '__main__':
    finder = PathFinder()
    finder.load_file('input.txt')
    finder.follow_path()
    print(finder.password)
    
    finder.cube = True
    finder.load_file('input.txt')
    finder.follow_path()
    print(finder.password)
    finder.print_map()

