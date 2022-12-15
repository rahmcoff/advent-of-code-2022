import unittest


class TestToday(unittest.TestCase):
    def test_part_1(self):
        sim = SandSimulation()
        sim.load_file('test_input.txt')
        sim.print_blocking()
        sim.drop_sand()
        sim.print_blocking()
        self.assertEqual(24, sim.grains_dropped)

    def test_part_2(self):
        sim = SandSimulation()
        sim.load_file('test_input.txt')
        sim.print_blocking()
        sim.drop_sand_with_floor()
        sim.print_blocking()
        self.assertEqual(93, sim.grains_dropped)


class SandSimulation:
    grains_dropped: int = 0
    blocked_paths: dict[int, set[int]]
    org_blocked_paths: dict[int, set[int]]
    starting_point = 500, 0
    max_row = 0
    
    def load_file(self, filename: str):
        self.blocked_paths = {}
        with open(filename) as f:
            for line in f:
                self.add_blocking_line(line.strip())
                
    def add_blocking_line(self, line: str):
        pieces = line.split(' -> ')
        for seg in range(len(pieces) - 1):
            col, row = [int(v) for v in pieces[seg].split(',')]
            n_col, n_row = [int(v) for v in pieces[seg+1].split(',')]
            self.max_row = max(self.max_row, row, n_row)
            
            if col == n_col:
                blocked_set = self.blocked_paths.setdefault(col, set())
                for i in range(min(row, n_row), max(row, n_row) + 1):
                    blocked_set.add(i)
            else:  # row == n_row
                for i in range(min(col, n_col), max(col, n_col) + 1):
                    self.blocked_paths.setdefault(i, set()).add(row)
        
        self.org_blocked_paths = {}
        for col, blocked in self.blocked_paths.items():
            self.org_blocked_paths[col] = blocked.copy()
                    
    def drop_sand(self):
        while self.track_sand(self.starting_point[0], self.starting_point[1]):
            self.grains_dropped += 1
            
    def drop_sand_with_floor(self):
        # does not reset so that we can keep the work already done
        while self.starting_point[1] not in self.blocked_paths[self.starting_point[0]]:
            self.track_sand(self.starting_point[0], self.starting_point[1], True)
            self.grains_dropped += 1
    
    def track_sand(self, col: int, row: int, use_floor=False) -> bool:
        if col not in self.blocked_paths:
            if use_floor:
                self.blocked_paths[col] = {self.max_row + 1}
                return True
            return False
        try:
            blocked_at = min(r for r in self.blocked_paths[col] if r > row)
        except ValueError:  # happens when seq is empty
            if use_floor:
                self.blocked_paths[col].add(self.max_row + 1)
            return False
        
        if blocked_at not in self.blocked_paths.get(col-1, ()):
            return self.track_sand(col - 1, blocked_at, use_floor)
        
        if blocked_at not in self.blocked_paths.get(col+1, ()):
            return self.track_sand(col + 1, blocked_at, use_floor)

        self.blocked_paths[col].add(blocked_at - 1)
        return True
        
    def print_blocking(self):
        x = 0
        cols = [k for k in self.blocked_paths.keys()]
        cols.sort()
        print(''.join('-' if c != self.starting_point[0] else '*' for c in cols))
        for x in range(self.max_row + 2):
            print(''.join(['#' if x in self.org_blocked_paths.get(c, ())
                           else 'o' if x in self.blocked_paths[c] else ' '
                           for c in cols]))
            
            
            
                


if __name__ == '__main__':
    s = SandSimulation()
    s.load_file('input.txt')
    s.print_blocking()
    s.drop_sand()
    print(s.grains_dropped)
    
    s.drop_sand_with_floor()
    s.print_blocking()
    print(s.grains_dropped)

