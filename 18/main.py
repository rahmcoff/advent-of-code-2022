import unittest


class TodayTest(unittest.TestCase):
    def test_part_1(self):
        test_drop = DropletAnalizer('test_input.txt')
        self.assertEqual(64, test_drop.get_surface_area())
    
    def test_part_2(self):
        test_drop = DropletAnalizer('test_input.txt')
        self.assertEqual(58, test_drop.get_outside_surface_area())


class DropletAnalizer:
    droplet: set[tuple[int, int, int]]
    interior: set[tuple[int, int, int]]
    exterior: set[tuple[int, int, int]]
    max_side = -1
    
    def __init__(self, filename: str):
        self.droplet = set()
        with open(filename) as f:
            for line in f:
                x, y, z = line.strip().split(',')
                self.droplet.add((int(x), int(y), int(z)))
                self.max_side = max(int(x), int(y), int(z), self.max_side)
    
    def get_surface_area(self) -> int:
        area = 0
        for point in self.droplet:
            for adjacent in self.get_adjacent_points(point):
                if adjacent not in self.droplet:
                    area += 1
        return area
    
    def get_adjacent_points(self, point: tuple[int, int, int]) -> list[tuple[int, int, int]]:
        x, y, z = point
        return [(x + 1, y, z),
                (x - 1, y, z),
                (x, y + 1, z),
                (x, y - 1, z),
                (x, y, z + 1),
                (x, y, z - 1)]
    
    def get_outside_surface_area(self) -> int:
        self.interior = set()
        self.exterior = set()
        area = 0
        for point in self.droplet:
            for adjacent in self.get_adjacent_points(point):
                if self.test(adjacent):
                    area += 1
        return area
    
    def test(self, point: tuple[int, int, int]) -> bool:
        if point in self.exterior:
            return True
        if point in self.interior or point in self.droplet:
            return False
        
        viewed_points = set(point)
        boundary_points = [point]
        
        while boundary_points:
            test_point = boundary_points.pop(0)
            for adjacent in self.get_adjacent_points(test_point):
                if adjacent in self.droplet or adjacent in viewed_points:
                    continue
                if adjacent in self.exterior:
                    self.exterior = self.exterior.union(viewed_points)
                    return True
                if adjacent in self.interior:
                    self.interior = self.interior.union(viewed_points)
                    return False
                viewed_points.add(adjacent)
                boundary_points.append(adjacent)
                for dim in adjacent:
                    if dim == 0 or dim == self.max_side:
                        self.exterior = self.exterior.union(viewed_points)
                        return True
        self.interior = self.interior.union(viewed_points)
        return False


if __name__ == '__main__':
    analyser = DropletAnalizer('input.txt')
    print(analyser.get_surface_area())
    print(analyser.get_outside_surface_area())
