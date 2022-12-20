import unittest


class TestToday(unittest.TestCase):
    sample_input = [1,
                    2,
                    -3,
                    3,
                    -2,
                    0,
                    4]
    
    def test_part_one(self):
        test_m = Mixer()
        test_m.initial_code = self.sample_input
        test_m.mix()
        self.assertEqual(test_m[1000], 4)
        self.assertEqual(test_m[2000], -3)
        self.assertEqual(test_m[3000], 2)
        
    def test_part_two(self):
        test_m = Mixer()
        test_m.initial_code = self.sample_input
        test_m.apply_decoding()
        test_m.mix(10)
        self.assertEqual(811589153, test_m[1000])
        self.assertEqual(2434767459, test_m[2000])
        self.assertEqual(-1623178306, test_m[3000])


class Mixer:
    initial_code: list[int]
    mixed_mapping: list[int]
    
    def load_file(self, filename: str):
        self.initial_code = []
        with open(filename) as f:
            for line in f:
                self.initial_code.append(int(line))
    
    def mix(self, iterations=1):
        self.mixed_mapping = [x for x in range(len(self.initial_code))]
        mod = len(self.mixed_mapping) - 1
        for _ in range(iterations):
            for map_pos, number in enumerate(self.initial_code):
                old_pos = self.mixed_mapping.index(map_pos)
                new_pos = (old_pos + number + mod) % mod
                del self.mixed_mapping[old_pos]
                self.mixed_mapping.insert(new_pos, map_pos)
    
    def __getitem__(self, item: int) -> int:
        mapped_zero = self.initial_code.index(0)
        pos = (self.mixed_mapping.index(mapped_zero) + item) % len(self.mixed_mapping)
        map_pos = self.mixed_mapping[pos]
        return self.initial_code[map_pos]

    def apply_decoding(self):
        self.initial_code = [x*811589153 for x in self.initial_code]


if __name__ == '__main__':
    mix = Mixer()
    mix.load_file('input.txt')
    mix.mix()
    print(mix[1000] + mix[2000] + mix[3000])
    
    mix.apply_decoding()
    mix.mix(10)
    print(mix[1000] + mix[2000] + mix[3000])
