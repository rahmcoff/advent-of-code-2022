import unittest
import re


class TodaysTest(unittest.TestCase):
    sample = ["$ cd /",
              "$ ls",
              "dir a",
              "14848514 b.txt",
              "8504156 c.dat",
              "dir d",
              "$ cd a",
              "$ ls",
              "dir e",
              "29116 f",
              "2557 g",
              "62596 h.lst",
              "$ cd e",
              "$ ls",
              "584 i",
              "$ cd ..",
              "$ cd ..",
              "$ cd d",
              "$ ls",
              "4060174 j",
              "8033020 d.log",
              "5626152 d.ext",
              "7214296 k"]
    expected_tree = {
        'files': {'b.txt': 14848514, 'c.dat': 8504156},
        'dirs': {
            'a': {
                'files': {'f': 29116, 'g': 2557, 'h.lst': 62596},
                'dirs': {
                    'e': {
                        'files': {'i': 584},
                        'dirs': {}
                    }
                }
            },
            'd': {
                'files': {'j': 4060174, 'd.log': 8033020, 'd.ext': 5626152, 'k': 7214296},
                'dirs': {}
            }
        }
    }
    
    def test_build_tree(self):
        self.assertEqual(build_tree(self.sample), self.expected_tree)
        
    def test_get_sizes(self):
        self.assertEqual(calculate_tree_size(self.expected_tree), {
            '/a/e/': 584,
            '/a/': 94853,
            '/d/': 24933642,
            '/': 48381165
        })
        

def build_tree(terminal: [str]) -> dict:
    curr_path = []
    tree = {'files': {}, 'dirs': {}}
    curr_dir = None
    
    for line in terminal:
        line = line.strip()
        if line == '$ cd /':
            # Move to base dir
            curr_path = []
            continue
        if line == '$ cd ..':
            # Move up a dir
            curr_path.pop()
            continue
        if line[:5] == '$ cd ':
            # move into dir
            curr_path.append(line[5:])
            continue
        if line == '$ ls':
            curr_dir = get_dir_from_path(tree, curr_path)
            continue
        
        if line[:4] == 'dir ':
            curr_dir['dirs'][line[4:]] = {'files': {}, 'dirs': {}}
            continue
        match = re.match(r'^(\d+) (.+)$', line)
        if match:
            curr_dir['files'][match[2]] = int(match[1])
            continue
        
        print(f'I don’t know what "{line}" is!!')
    
    return tree


def calculate_tree_size(tree: dict) -> dict:
    all_sizes = {}
    direct_sub_dir_sizes = 0
    for name, subdir in tree['dirs'].items():
        dir_sizes_dict = calculate_tree_size(subdir)
        for sub_dir_name, size in dir_sizes_dict.items():
            all_sizes[f"/{name}{sub_dir_name}"] = size
        direct_sub_dir_sizes += dir_sizes_dict['/']
        
    size = sum(tree['files'].values()) + direct_sub_dir_sizes
    all_sizes['/'] = size
    return all_sizes


def get_dir_from_path(tree, curr_path: [str]) -> dict:
    curr_dir = tree
    for directory in curr_path:
        curr_dir = curr_dir['dirs'][directory]
    return curr_dir


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        terminal = f.readlines()
    
    tree = build_tree(terminal)
    dir_sizes = calculate_tree_size(tree)

    print(sum(s for s in dir_sizes.values() if s <= 100000))
    
    needed_space = 30000000 - (70000000 - dir_sizes['/'])
    print(min(s for s in dir_sizes.values() if s >= needed_space))
    