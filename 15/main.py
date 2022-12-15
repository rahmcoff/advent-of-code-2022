import unittest
from time import perf_counter_ns


class TestToday(unittest.TestCase):
    def test_part_1(self):
        test = SensorBlock()
        test.load_file('test_input.txt')
        self.assertEqual(26, test.blocked_at(10))
    
    def test_part_2(self):
        test = SensorBlock()
        test.load_file('test_input.txt')
        self.assertEqual((14, 11), test.find_free_space(0, 20))


class SensorBlock:
    sensors: list[tuple[int, int, int]]  # x, y, distance
    beacons: set[tuple[int, int]]
    
    def load_file(self, filename: str):
        self.sensors = []
        self.beacons = set()
        with open(filename) as f:
            for line in f:
                s_data, b_data = line.replace('Sensor at x=', '').split(': closest beacon is at x=')
                sensor_x, sensor_y = [int(s) for s in s_data.split(', y=')]
                beacon_x, beacon_y = [int(b) for b in b_data.split(', y=')]
                self.sensors.append((sensor_x, sensor_y, abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)))
                self.beacons.add((beacon_x, beacon_y))
    
    def update_ranges(self, ranges: set[tuple[int, int]], y: int, sensor: tuple[int, int, int],
                      min_val: int = None, max_val: int = None):
        sx, sy, distance = sensor
        if abs(sy - y) > distance:
            return
        minx = sx - (distance - abs(sy - y))
        maxx = sx + (distance - abs(sy - y))
        if any(r[0] <= minx and r[1] >= maxx for r in ranges):
            return
        overlap_low = [r for r in ranges if r[0] <= minx <= r[1]]
        if overlap_low:
            r = overlap_low[0]
            minx = r[0]
            ranges.remove(r)
        overlap_high = [r for r in ranges if r[0] <= maxx <= r[1]]
        if overlap_high:
            r = overlap_high[0]
            maxx = r[1]
            ranges.remove(r)
        overlap_both = [r for r in ranges if r[0] >= minx and r[1] <= maxx]
        for r in overlap_both:
            ranges.remove(r)
        if min_val is not None and minx < min_val:
            minx = min_val
        if max_val is not None and maxx > max_val:
            maxx = max_val
        ranges.add((minx, maxx))
    
    def blocked_at(self, y: int) -> int:
        ranges: set[tuple[int, int]] = set()
        for sensor in self.sensors:
            self.update_ranges(ranges, y, sensor)
        return sum(r[1] - r[0] + 1 for r in ranges) - len([b for b in self.beacons if b[1] == y])
    
    def find_free_space(self, min_val: int, max_val: int) -> tuple[int, int]:
        ranges: dict[int, set[tuple[int, int]]] = {}
        for sensor in self.sensors:
            for y in range(max(min_val, sensor[1] - sensor[2]), min(max_val, sensor[1] + sensor[2]) + 1):
                r = ranges.setdefault(y, set())
                if r == {(min_val, max_val)}:
                    continue
                self.update_ranges(r, y, sensor, min_val, max_val)
        for y in range(min_val, max_val+1):
            r = ranges[y]
            if r == {(min_val, max_val)}:
                continue
            if min_val not in (s[0] for s in r):
                return min_val, y
            return min(s[1] for s in r) + 1, y


if __name__ == '__main__':
    block = SensorBlock()
    block.load_file('input.txt')
    print(block.blocked_at(2000000))
    
    start = perf_counter_ns()
    free = block.find_free_space(0, 4000000)
    time = perf_counter_ns() - start
    print(f"{free}: {free[0] * 4000000 + free[1]}  {time/1000}sec")
