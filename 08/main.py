import unittest


class TodayTest(unittest.TestCase):
    sample = ['30373',
              '25512',
              '65332',
              '33549',
              '35390']
    sample_result = 21
    
    def test_count_visible_trees(self):
        self.assertEqual(count_visible_trees(self.sample), self.sample_result)
        
    alt_sample = ['111111',
                  '122221',
                  '155431',
                  '122221']
        
    def test_best_tree_count(self):
        self.assertEqual(best_tree_count(self.sample), 8)
        self.assertEqual(best_tree_count(self.alt_sample), 7)


def count_visible_trees(tree_rows: [str]):
    forest = get_forest(tree_rows)

    height = len(forest)
    width = len(forest[0])
    visible_forest = [[False] * width for i in range(height)]
    
    for row in range(height):
        tallest_tree = -1
        # from the left
        for col in range(width):
            tree = forest[row][col]
            if tree > tallest_tree:
                visible_forest[row][col] = True
                tallest_tree = tree
        
        tallest_tree = -1
        # from the right
        for col in range(width-1, 0, -1):
            tree = forest[row][col]
            if tree > tallest_tree:
                visible_forest[row][col] = True
                tallest_tree = tree

    for col in range(width):
        tallest_tree = -1
        # from the top
        for row in range(height):
            tree = forest[row][col]
            if tree > tallest_tree:
                visible_forest[row][col] = True
                tallest_tree = tree
    
        tallest_tree = -1
        # from the bottom
        for row in range(height - 1, 0, -1):
            tree = forest[row][col]
            if tree > tallest_tree:
                visible_forest[row][col] = True
                tallest_tree = tree
                
    return sum(row.count(True) for row in visible_forest)


def get_forest(tree_rows: [str]) -> [[int]]:
    forest: [[int]] = []
    for row in tree_rows:
        row = row.strip()
        forest_row = []
        for size in row:
            forest_row.append(int(size))
        forest.append(forest_row)
    return forest


def best_tree_count(tree_rows: [str]) -> int:
    forest = get_forest(tree_rows)
    
    height = len(forest)
    width = len(forest[0])
    best_count = 0
    
    for row in range(height):
        for col in range(width):
            tree = forest[row][col]
            tree_count = 1
            # looking up
            dir_count = 0
            for dir_count in range(1, row + 1):
                if forest[row - dir_count][col] >= tree:
                    break
            tree_count *= dir_count
            
            # looking down
            dir_count = 0
            for dir_count in range(1, height - row):
                if forest[row + dir_count][col] >= tree:
                    break
            tree_count *= dir_count
            
            # looking left
            dir_count = 0
            for dir_count in range(1, col + 1):
                if forest[row][col - dir_count] >= tree:
                    break
            tree_count *= dir_count
            
            # looking right
            dir_count = 0
            for dir_count in range(1, width - col):
                if forest[row][col + dir_count] >= tree:
                    break
            tree_count *= dir_count

            if tree_count > best_count:
                best_count = tree_count
                print(f"height: {tree}, row:{row}, col:{col}")
    return best_count



if __name__ == '__main__':
    with open('input.txt') as f:
        forest = f.readlines()
        
    print(count_visible_trees(forest))
    print(best_tree_count(forest))
