import time
import unittest


class TestToday(unittest.TestCase):
    def test_part_1(self):
        v = StormValley()
        v.load_file('test_input.txt')
        v.print_steps = True
        self.assertEqual(18, v.find_way_out())
    
    def test_part_2(self):
        v = StormValley()
        v.load_file('test_input.txt')
        self.assertEqual(54, v.find_way_out() + v.find_way_back() + v.find_way_out() - 2)


class StormValley:
    storms: list[tuple[int, int, str]]
    storms_by_pos: dict[tuple[int, int], list[str]]
    expeditions: set[tuple[int, int]]
    width: int
    height: int
    print_steps = False
    
    def load_file(self, filename):
        self.max_expeditions = 0
        self.storms = []
        with open(filename) as f:
            for row, line in enumerate(f):
                line = line.strip('#\n\r')
                row -= 1
                if len(line) < 3:
                    continue
                for col, letter in enumerate(line):
                    if letter == '.':
                        continue
                    self.storms.append((row, col, letter))
            self.width = col + 1
        self.height = row
    
    def next_minute(self):
        self.storms_by_pos = {}
        for index, (row, col, dir) in enumerate(self.storms):
            if dir == '^':
                row = (row - 1) % self.height
            elif dir == '>':
                col = (col + 1) % self.width
            elif dir == 'v':
                row = (row + 1) % self.height
            elif dir == '<':
                col = (col - 1) % self.width
            self.storms[index] = row, col, dir
            self.storms_by_pos.setdefault((row, col), []).append(dir)
        
        next_expeditions = set()
        for row, col in self.expeditions:
            if (row, col) not in self.storms_by_pos:
                next_expeditions.add((row, col))
            if row > 0 and (row - 1, col) not in self.storms_by_pos:
                next_expeditions.add((row - 1, col))
            if col > 0 and (row, col - 1) not in self.storms_by_pos:
                next_expeditions.add((row, col - 1))
            if row < self.height - 1 and (row + 1, col) not in self.storms_by_pos:
                next_expeditions.add((row + 1, col))
            if col < self.width - 1 and (row, col + 1) not in self.storms_by_pos:
                next_expeditions.add((row, col + 1))
        if len(next_expeditions) > self.max_expeditions:
            self.max_expeditions = len(next_expeditions)
        self.expeditions = next_expeditions
    
    def find_way_out(self) -> int:
        self.expeditions = set()
        minutes = 0
        
        while (self.height - 1, self.width - 1) not in self.expeditions:
            minutes += 1
            self.next_minute()
            if (0, 0) not in self.storms_by_pos:
                self.expeditions.add((0, 0))
            if self.print_steps:
                print(f' - {minutes} -')
                self.print_valley()
        return minutes + 1
    
    def find_way_back(self) -> int:
        self.expeditions = set()
        minutes = 0
        
        while (0, 0) not in self.expeditions:
            minutes += 1
            self.next_minute()
            if (self.height - 1, self.width - 1) not in self.storms_by_pos:
                self.expeditions.add((self.height - 1, self.width - 1))
            if self.print_steps:
                print(f' - {minutes} -')
                self.print_valley()
        return minutes + 1
    
    def print_valley(self):
        for row in range(self.height):
            line = []
            for col in range(self.width):
                storms = self.storms_by_pos.get((row, col), [])
                if len(storms) > 1:
                    line.append(str(len(storms)))
                elif storms:
                    line.append(storms[0])
                elif (row, col) in self.expeditions:
                    line.append('E')
                else:
                    line.append('.')
            print(''.join(line))


if __name__ == '__main__':
    valley = StormValley()
    valley.load_file('input.txt')
    start = time.process_time()
    minutes_out = valley.find_way_out()
    print(f"{minutes_out} took {time.process_time() - start} sec")
    print(f"{minutes_out + valley.find_way_back() + valley.find_way_out() - 2} max {valley.max_expeditions} took {time.process_time() - start}")
