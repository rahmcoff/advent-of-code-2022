import time
import unittest


class TestToday(unittest.TestCase):
    def test_part_1(self):
        t = ElfSpread()
        t.load_file('test_input.txt')
        t.spread_out(10)
        t.print()
        self.assertEqual(110, t.get_empty_spaces())

    def test_part_2(self):
        t = ElfSpread()
        t.load_file('test_input.txt')
        t.spread_out()
        self.assertEqual(20, t.total_rounds)
        t.print()


class ElfSpread:
    check_order: list[str]
    elves = set[tuple[int, int]]
    total_rounds = 0
    
    def load_file(self, filename):
        self.elves = set()
        with open(filename) as f:
            for row, line in enumerate(f):
                for col, letter in enumerate(line):
                    if letter == '#':
                        self.elves.add((row, col))
        self.check_order = ['N', 'S', 'W', 'E']
        self.total_rounds = 0
    
    def spread_out(self, count: int = None):
        if count is None:
            count = 10000000
        
        for round in range(count):
            proposed_moves = {}
            doubled_proposed = {}
            for elf_number, current_pos in enumerate(self.elves):
                new_pos = self.get_proposed(current_pos)
                if new_pos:
                    if new_pos not in doubled_proposed:
                        proposed_moves[current_pos] = new_pos
                        doubled_proposed[new_pos] = current_pos
                    else:
                        other_pos = doubled_proposed[new_pos]
                        del proposed_moves[other_pos]
            if not proposed_moves:
                break
            for old_pos, new_pos in proposed_moves.items():
                self.elves.remove(old_pos)
                self.elves.add(new_pos)
            self.check_order.append(self.check_order.pop(0))
        self.total_rounds = round + 1
    
    def get_proposed(self, current_pos: tuple[int, int]) -> tuple[int, int] | None:
        adjacent = [
            (current_pos[0] - 1, current_pos[1] - 1), (current_pos[0] - 1, current_pos[1]), (current_pos[0] - 1, current_pos[1] + 1),
            (current_pos[0], current_pos[1] - 1), (current_pos[0], current_pos[1] + 1),
            (current_pos[0] + 1, current_pos[1] - 1), (current_pos[0] + 1, current_pos[1]), (current_pos[0] + 1, current_pos[1] + 1),
        ]
        if not any(pos in self.elves for pos in adjacent):
            return None
        for direction in self.check_order:
            if direction == 'N':
                adjacent = [(current_pos[0] - 1, current_pos[1] - 1), (current_pos[0] - 1, current_pos[1]), (current_pos[0] - 1, current_pos[1] + 1)]
                new_pos = (current_pos[0] - 1, current_pos[1])
            elif direction == 'S':
                adjacent = [(current_pos[0] + 1, current_pos[1] - 1), (current_pos[0] + 1, current_pos[1]), (current_pos[0] + 1, current_pos[1] + 1)]
                new_pos = (current_pos[0] + 1, current_pos[1])
            elif direction == 'W':
                adjacent = [(current_pos[0] - 1, current_pos[1] - 1), (current_pos[0], current_pos[1] - 1), (current_pos[0] + 1, current_pos[1] - 1)]
                new_pos = (current_pos[0], current_pos[1] - 1)
            else:
                adjacent = [(current_pos[0] - 1, current_pos[1] + 1), (current_pos[0], current_pos[1] + 1), (current_pos[0] + 1, current_pos[1] + 1)]
                new_pos = (current_pos[0], current_pos[1] + 1)
            if not any(pos in self.elves for pos in adjacent):
                return new_pos

        return None

    def get_empty_spaces(self) -> int:
        n, s, e, w = self.get_bounding_rect()
        return (s - n + 1) * (e - w + 1) - len(self.elves)

    def print(self):
        n, s, e, w = self.get_bounding_rect()
        for row in range(n, s+1):
            line = []
            for col in range(w, e+1):
                line.append('#' if (row, col) in self.elves else '.')
            print(''.join(line))

    def get_bounding_rect(self) -> tuple[int, int, int, int]:
        """Returns N, S, E, W"""
        n = s = w = e = None
        
        for pos in self.elves:
            if n is None or n > pos[0]:
                n = pos[0]
            if s is None or s < pos[0]:
                s = pos[0]
            if w is None or w > pos[1]:
                w = pos[1]
            if e is None or e < pos[1]:
                e = pos[1]
        return n, s, e, w


if __name__ == '__main__':
    elf_tracker = ElfSpread()
    elf_tracker.load_file('input.txt')
    start = time.process_time()
    elf_tracker.spread_out(10)
    print(f'{elf_tracker.get_empty_spaces()} took {time.process_time() - start}')
    elf_tracker.spread_out()
    elf_tracker.print()
    print(f'{elf_tracker.total_rounds} took {time.process_time() - start}')
