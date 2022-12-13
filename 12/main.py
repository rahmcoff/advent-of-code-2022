import unittest

class TodayTest(unittest.TestCase):
    def test_find_shortest(self):
        p = Pathfinder()
        p.load_file('test_input.txt')
        p.find_routes()
        p.print_distances()
        self.assertEqual(31, p.end_distance)


class Pathfinder:
    start_pos: tuple[int, int] = None
    end_pos: tuple[int, int] = None
    height_grid: list[list[int]] = None
    distances: dict[tuple[int, int], int] = None
    updated_nodes: list[tuple[int, int]]
    
    def load_file(self, filename: str):
        self.height_grid = []
        self.distances = {}
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                height_line = []
                for letter in line:
                    if letter == 'S':
                        self.start_pos = (len(self.height_grid), len(height_line))
                        height_line.append(0)
                    elif letter == 'E':
                        self.end_pos = (len(self.height_grid), len(height_line))
                        height_line.append(25)
                    else:
                        height_line.append(ord(letter) - ord('a'))
                self.height_grid.append(height_line)
    
    def find_routes(self):
        self.distances = {self.start_pos: 0}
        self.updated_nodes = [self.start_pos]

        while self.updated_nodes:
            current_node = self.updated_nodes.pop(0)
            self.test_node(current_node, (current_node[0] - 1, current_node[1]))
            self.test_node(current_node, (current_node[0] + 1, current_node[1]))
            self.test_node(current_node, (current_node[0], current_node[1] - 1))
            self.test_node(current_node, (current_node[0], current_node[1] + 1))

    def test_node(self, current_node: tuple[int, int], new_node: tuple[int, int]):
        if not (0 <= new_node[0] < len(self.height_grid)) or \
           not (0 <= new_node[1] < len(self.height_grid[0])):
            return
        
        current_height = self.height_grid[current_node[0]][current_node[1]]
        new_height = self.height_grid[new_node[0]][new_node[1]]
        if new_height > current_height + 1:
            return
        if new_height == 0 and new_node[1] > 1:
            return
        
        current_distance = self.distances[current_node]
        if self.end_distance and self.end_distance <= current_distance:
            return
        node_distance = self.distances.get(new_node)
        if node_distance is None or node_distance > current_distance + 1:
            self.distances[new_node] = current_distance + 1
            self.updated_nodes.append(new_node)
    
    def print_distances(self):
        for row, line in enumerate(self.height_grid):
            print('  '.join([f'{height: >2} {self.distances.get((row, col), "-")!s: >3}'
                             for col, height in enumerate(line)
                             ]))

    @property
    def end_distance(self) -> int|None:
        return self.distances.get(self.end_pos)


if __name__ == '__main__':
    p = Pathfinder()
    p.load_file('input.txt')
    p.find_routes()
    p.print_distances()
    print(p.end_distance)
    
    distances = []
    for i in range(len(p.height_grid)):
        p.start_pos = (i, 0)
        p.find_routes()
        distances.append(p.end_distance)
    print(distances)
    print(min(distances))

