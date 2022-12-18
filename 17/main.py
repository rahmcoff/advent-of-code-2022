import unittest


class TodayTest(unittest.TestCase):
    sample_blow = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
    
    def test_part_1(self):
        test_board = Tetris(self.sample_blow)
        test_board.run_blocks(10)
        test_board.print_board()
        test_board.run_blocks(2022)
        self.assertEqual(3068, len(test_board.board))
        test_board.find_repeats()
        
        self.assertEqual(1514285714288, test_board.run_blocks(1000000000000))

    

class Block:
    left: int
    bottom: int
    width: int
    
    def get_pieces(self) -> list[tuple[int, int]]:
        pass
    
    def __init__(self, height):
        self.left = 2
        self.bottom = height + 3
    
    def blow_right(self, board: list[set[int]]):
        if self.left + self.width >= 7:
            return
        if self.bottom < len(board):
            for l, b in self.get_pieces():
                if b < len(board) and l + 1 in board[b]:
                    return
        self.left += 1
    
    def blow_left(self, board: list[set[int]]):
        if self.left == 0:
            return
        if self.bottom < len(board):
            for l, b in self.get_pieces():
                if b < len(board) and l - 1 in board[b]:
                    return
        self.left -= 1
    
    def drop(self, board: list[set[int]]) -> bool:
        if self.bottom == 0:
            self.settle(board)
            return False
        if self.bottom - 1 < len(board):
            for l, b in self.get_pieces():
                if b - 1 < len(board) and l in board[b - 1]:
                    self.settle(board)
                    return False
        self.bottom -= 1
        return True
    
    def settle(self, board: list[set[int]]):
        for l, b in self.get_pieces():
            if b >= len(board):
                board.append({l})
            else:
                board[b].add(l)


class BlockMinus(Block):
    width = 4
    
    def get_pieces(self) -> list[tuple[int, int]]:
        return [(self.left + n, self.bottom) for n in range(4)]


class BlockPlus(Block):
    width = 3
    
    def get_pieces(self) -> list[tuple[int, int]]:
        return [(self.left + 1, self.bottom),
                (self.left, self.bottom + 1), (self.left + 1, self.bottom + 1), (self.left + 2, self.bottom + 1),
                (self.left + 1, self.bottom + 2)]


class BlockL(Block):
    width = 3
    
    def get_pieces(self) -> list[tuple[int, int]]:
        return [(self.left, self.bottom), (self.left + 1, self.bottom), (self.left + 2, self.bottom),
                (self.left + 2, self.bottom + 1),
                (self.left + 2, self.bottom + 2)]


class BlockI(Block):
    width = 1
    
    def get_pieces(self) -> list[tuple[int, int]]:
        return [(self.left, self.bottom + n) for n in range(4)]


class BlockSquare(Block):
    width = 2
    
    def get_pieces(self) -> list[tuple[int, int]]:
        return [(self.left, self.bottom), (self.left + 1, self.bottom),
                (self.left, self.bottom + 1), (self.left + 1, self.bottom + 1)]


class Tetris:
    blow_pattern: str
    board: list[set[int]]
    
    block_pattern = [BlockMinus, BlockPlus, BlockL, BlockI, BlockSquare]
    
    def __init__(self, blow_pattern: str):
        self.blow_pattern = blow_pattern
        self.repeating_blocks = self.repeating_lines = None
        
    def run_blocks(self, number=2022):
        if self.repeating_lines:
            lines_to_add_from_repeating = self.repeating_lines * (number // self.repeating_blocks - 1)
            number = number % self.repeating_blocks + self.repeating_blocks
        else:
            lines_to_add_from_repeating = 0
        
        self.board = []
        blow_index = 0
        for block_index in range(number):
            block = self.block_pattern[block_index % len(self.block_pattern)](len(self.board))
            while True:
                if self.blow_pattern[blow_index] == '>':
                    block.blow_right(self.board)
                else:
                    block.blow_left(self.board)
                blow_index = (blow_index + 1) % len(self.blow_pattern)
                
                if not block.drop(self.board):
                    break
                    
        return len(self.board) + lines_to_add_from_repeating
    
    def print_board(self):
        for i in range(len(self.board) - 1, -1, -1):
            print(''.join(['#' if n in self.board[i] else '.' for n in range(7)]))
            
    def find_repeats(self):
        for i in range(5, len(self.board) // 3):
            if self.board[-2 * i: -i] == self.board[-3 * i: -2 * i]:
                self.repeating_lines = i
                self.repeating_blocks = sum(len(l) for l in self.board[-i-5:-5])
                if self.repeating_blocks % 22 > 0:
                    continue
                self.repeating_blocks = self.repeating_blocks * 5 // 22
                print(f"repeats every {i} lines with {sum(len(l) for l in self.board[-i-5:-5]) * 5 / 22} blocks")
                break
                


if __name__ == '__main__':
    with open('input.txt') as f:
        game = Tetris(f.readline().strip())
        
    game.run_blocks(2022)
    print(len(game.board))
    game.run_blocks(202200)
    game.find_repeats()
    print(game.run_blocks(1000000000000))
