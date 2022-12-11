import unittest
from monk import Monkey


class TodayTest(unittest.TestCase):
    def test_single_round(self):
        from test_input import monkeys
        jung = Jungle(monkeys)
        jung.run_round()
        self.assertEqual(jung.monkeys[0].objects, [20, 23, 27, 26])
        self.assertEqual(jung.monkeys[1].objects, [2080, 25, 167, 207, 401, 1046])
        self.assertEqual(jung.monkeys[2].objects, [])
        self.assertEqual(jung.monkeys[3].objects, [])

    def test_full_game(self):
        from test_input import monkeys
        jung = Jungle(monkeys)
        jung.run_game()
        self.assertEqual(jung.monkeys[0].objects, [10, 12, 14, 26, 34])
        self.assertEqual(jung.monkeys[1].objects, [245, 93, 53, 199, 115])
        self.assertEqual(jung.monkeys[2].objects, [])
        self.assertEqual(jung.monkeys[3].objects, [])
        self.assertEqual(jung.monkeys[0].objects_seen, 101)
        self.assertEqual(jung.monkeys[1].objects_seen, 95)
        self.assertEqual(jung.monkeys[2].objects_seen, 7)
        self.assertEqual(jung.monkeys[3].objects_seen, 105)
        
    def test_part_2(self):
        from test_input import monkeys
        jung = Jungle(monkeys)
        jung.run_game()
        self.assertEqual(jung.monkeys[0].objects_seen, 52166)
        self.assertEqual(jung.monkeys[1].objects_seen, 47830)
        self.assertEqual(jung.monkeys[2].objects_seen, 1938)
        self.assertEqual(jung.monkeys[3].objects_seen, 52013)




class Jungle:
    def __init__(self, monkeys: [Monkey]):
        self.monkeys = monkeys
        
    def run_round(self):
        for monkey in self.monkeys:
            while True:
                next_object = monkey.process_next_object()
                if next_object is None:
                    break
                self.monkeys[next_object[1]].objects.append(next_object[0])
                
    def run_game(self):
        for _ in range(10000):
            self.run_round()


if __name__ == '__main__':
    from input import monkeys
    jung = Jungle(monkeys)
    jung.run_game()
    
    seen = [m.objects_seen for m in jung.monkeys]
    seen.sort(reverse=True)
    print(seen[0] * seen[1])
