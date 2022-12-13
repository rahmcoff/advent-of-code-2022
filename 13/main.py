import unittest
import json
from functools import cmp_to_key


class TestToday(unittest.TestCase):
    def test_part_1(self):
        p = MessageParser()
        p.load_file('test_input.txt')
        p.compare_messages()
        self.assertEqual([1, 2, 4, 6], p.correct_pairs)
    
    part_2_result = [[],
                     [[]],
                     [[[]]],
                     [1, 1, 3, 1, 1],
                     [1, 1, 5, 1, 1],
                     [[1], [2, 3, 4]],
                     [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
                     [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
                     [[1], 4],
                     [[2]],
                     [3],
                     [[4, 4], 4, 4],
                     [[4, 4], 4, 4, 4],
                     [[6]],
                     [7, 7, 7],
                     [7, 7, 7, 7],
                     [[8, 7, 6]],
                     [9]]
    
    def test_part_2(self):
        p = MessageParser()
        p.load_file('test_input.txt')
        p.sort_messages()
        self.assertEqual(self.part_2_result, p.all_messages)


class MessageParser():
    pairs: list[tuple[list, list]] = None
    correct_pairs: list[int] = None
    all_messages: list[list] = None
    
    def load_file(self, filename: str):
        with open(filename) as f:
            data = [line.strip() for line in f]
        
        self.pairs = []
        self.all_messages = [
            [[2]],
            [[6]]
        ]
        for line_number in range(0, len(data), 3):
            l = json.loads(data[line_number])
            r = json.loads(data[line_number + 1])
            self.pairs.append(
                (l, r)
            )
            self.all_messages.append(l)
            self.all_messages.append(r)
    
    def compare_messages(self):
        self.correct_pairs = []
        for i, pair in enumerate(self.pairs):
            if self.compare_lists(pair[0], pair[1]):
                self.correct_pairs.append(i + 1)
    
    def compare_lists(self, left: list[list | int], right: list[list | int]) -> bool | None:
        i = 0
        while True:
            if i >= len(left) and i >= len(right):
                return None
            if i >= len(left):
                return True
            if i >= len(right):
                return False
            
            l, r = left[i], right[i]
            
            if l == r:
                i += 1
                continue
            
            if isinstance(l, int) and isinstance(r, int):
                return l <= r
            
            if isinstance(l, int) and isinstance(r, list):
                l = [l]
            if isinstance(left[i], list) and isinstance(r, int):
                r = [r]
            
            result = self.compare_lists(l, r)
            if result is None:
                i += 1
                continue
            return result
        
    def cmp_function(self, l, r):
        return -1 if self.compare_lists(l, r) else 1
        
    def sort_messages(self):
        self.all_messages.sort(key=cmp_to_key(self.cmp_function))


if __name__ == '__main__':
    p = MessageParser()
    p.load_file('input.txt')
    p.compare_messages()
    print(p.correct_pairs)
    print(sum(p.correct_pairs))
    
    p.sort_messages()
    index_2 = p.all_messages.index([[2]]) + 1
    index_6 = p.all_messages.index([[6]]) + 1
    print(p.all_messages)
    print(f"{index_2}*{index_6}={index_2*index_6}")
