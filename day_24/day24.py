import sys
from collections import namedtuple
import heapq



DIR_VECTOR = {
    'UP': (-1, 0),
    'DOWN': (1, 0),
    'LEFT': (0, -1),
    'RIGHT': (0, 1)
}

DIR = {
    '^': 'UP',
    'v': 'DOWN',
    '<': 'LEFT',
    '>': 'RIGHT'
}


def print_map(grid, blizzards):
    grid.clean()
    for bliz in blizzards:
        r, c, dir = bliz.position
        if dir == 'UP':
            grid.set_cell(r, c, '^')
        if dir == 'DOWN':
            grid.set_cell(r, c, 'v')
        elif dir == 'LEFT':
            grid.set_cell(r, c, '<')
        elif dir == 'RIGHT':
            grid.set_cell(r, c, '>')
    
    grid.print()


class Board:
    def __init__(self, grid, blizzards) -> None:
        self.grid = grid
        self.blizzards = blizzards
        self.height = len(grid)
        self.width = len(grid[0])

    def is_free(self, row, col):
        for blizz in self.blizzards:
            r, c, _ = blizz.position
            if r == row and c == col:
                return False
        return True

    def advance_blizzards(self):
        for blizz in self.blizzards:
            row, col, dir = blizz.position
            vector = DIR_VECTOR[dir]
            dr, dc = vector
            new_row = row if dr == 0 else (row + dr) % (self.height - 1)
            new_col = col if dc == 0 else (col + dc) % (self.width - 1)
            
            if new_col == 0 and dir == 'RIGHT':
                new_col += 1
            elif new_col == 0 and dir == 'LEFT':
                new_col += (self.width - 2)
            
            if new_row == 0 and dir == 'UP':
                new_row += (self.height - 2)
            elif new_row == 0 and dir == 'DOWN':
                new_row += 1

            blizz.update(new_row, new_col, dir)

    def adj(self, row, col, allow_wait=False, coming_back=False):
        neighbours = set()
        for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            rr, cc = row + dr, col + dc
            # this is the destination
            if rr == self.height - 1 and cc == self.width - 2:
                neighbours.add((rr, cc))
            if rr == 0 and cc == 1 and coming_back:
                neighbours.add((rr, cc))
            # within bounds
            elif 1 <= rr <= self.height - 2 and 1 <= cc <= self.width - 2:
                if self.is_free(rr, cc):
                    neighbours.add((rr, cc))
        if allow_wait and self.is_free(row, col):
            neighbours.add((row, col))
        return neighbours


class Blizzard:
    def __init__(self, row, col, dir) -> None:
        self.row = row
        self.col = col
        self.dir = dir

    def update(self, row, col, dir):
        self.row = row
        self.col = col
        self.dir = dir

    @property
    def position(self):
        return self.row, self.col, self.dir


def parse_input(sample):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'
    
    with open(filename) as f:
        lines = f.read().splitlines()
    
    grid = []
    for line in lines:
        line = line.replace('#', ' ')
        grid.append(list(line))
    
    blizzards = []
    for i, row in enumerate(grid):
        for j, _ in enumerate(row):
            if grid[i][j] not in [' ', '.']:
                blizzards.append(Blizzard(i, j, DIR[grid[i][j]]))

    return grid, blizzards

def part1(board: Board, verbose=False):
    start = (0, 1)
    dest = (board.height - 1, len(board.grid[-1]) - 2)
    print(dest)

    i = 0
    seen = {start}
    while dest not in seen and i < 50:
        i += 1
        # before advancing the blizzards everything in seen must be free
        for position in seen:
            assert board.is_free(*position)
        board.advance_blizzards()
        new_seen = set()
        for position in seen:
            possible_moves = board.adj(*position, allow_wait=True)
            new_seen.update(possible_moves)
        seen = new_seen

    print(i)

def part2(board: Board, verbose=False):
    start = (0, 1)
    dest = (board.height - 1, len(board.grid[-1]) - 2)
    print(dest)

    i = 0
    seen = {start}
    while dest not in seen:
        i += 1
        # before advancing the blizzards everything in seen must be free
        # for position in seen:
        #     assert board.is_free(*position)
        board.advance_blizzards()
        new_seen = set()
        for position in seen:
            possible_moves = board.adj(*position, allow_wait=True)
            new_seen.update(possible_moves)
        seen = new_seen

    print(i)

    seen = {dest}
    while start not in seen:
        i += 1
        # for position in seen:
        #     assert board.is_free(*position)
        board.advance_blizzards()
        new_seen = set()
        for position in seen:
            possible_moves = board.adj(*position, allow_wait=True, coming_back=True)
            new_seen.update(possible_moves)
        seen = new_seen

    seen = {start}
    while dest not in seen:
        i += 1
        # for position in seen:
        #     assert board.is_free(*position)
        board.advance_blizzards()
        new_seen = set()
        for position in seen:
            possible_moves = board.adj(*position, allow_wait=True)
            new_seen.update(possible_moves)
        seen = new_seen

    print(i)

def blizzard_tests():
    grid = [
        # 0 , 1  ,  2 ,  3 ,  4 ,  5 ,  6 ,  7 ,  8 ,  9 , 10
        [' ', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], # 0
        [' ', '.', '.', '.', '.', '.', '.', '.', '.', '.', ' '], # 1
        [' ', '>', '.', '.', '.', '.', '.', '.', '.', '.', ' '], # 2
        [' ', '.', '.', '.', '.', '.', '.', '.', '.', '.', ' '], # 3
        [' ', '.', '.', '.', '.', '.', '.', '.', 'v', '.', ' '], # 4
        [' ', '.', '.', '.', '.', '.', '.', '.', '.', '.', ' '], # 5
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '.', ' ']  # 6
    ]

    
    # test 1 movement in each direction without wrap
    blizzard = Blizzard(2, 1, DIR['>'])
    board = Board(grid, [blizzard])
    board.advance_blizzards()
    assert blizzard.position == (2, 2, DIR['>'])

    blizzard = Blizzard(2, 3, DIR['<'])
    board = Board(grid, [blizzard])
    board.advance_blizzards()
    assert blizzard.position == (2, 2, DIR['<'])

    blizzard = Blizzard(3, 2, DIR['^'])
    board = Board(grid, [blizzard])
    board.advance_blizzards()
    assert blizzard.position == (2, 2, DIR['^'])
    
    blizzard = Blizzard(3, 2, DIR['v'])
    board = Board(grid, [blizzard])
    board.advance_blizzards()
    assert blizzard.position == (4, 2, DIR['v'])

    # test 1 movement in each direction with wrap
    blizzard = Blizzard(2, 9, DIR['>'])
    board = Board(grid, [blizzard])
    board.advance_blizzards()
    assert blizzard.position == (2, 1, DIR['>'])

    blizzard = Blizzard(2, 1, DIR['<'])
    board = Board(grid, [blizzard])
    board.advance_blizzards()
    assert blizzard.position == (2, 9, DIR['<'])

    blizzard = Blizzard(1, 2, DIR['^'])
    board = Board(grid, [blizzard])
    board.advance_blizzards()
    assert blizzard.position == (5, 2, DIR['^'])

    blizzard = Blizzard(5, 2, DIR['v'])
    board = Board(grid, [blizzard])
    board.advance_blizzards()
    assert blizzard.position == (1, 2, DIR['v'])



def neighbour_tests():
    grid = [
        # 0 , 1  ,  2 ,  3 ,  4 ,  5 ,  6 ,  7 ,  8 ,  9 , 10
        [' ', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], # 0
        [' ', '.', '.', '.', '.', '.', '.', '.', '.', '.', ' '], # 1
        [' ', '>', '.', '.', '.', '.', '.', '.', '.', '.', ' '], # 2
        [' ', '.', '.', '.', '.', '.', '.', '.', '.', '.', ' '], # 3
        [' ', '.', '.', '.', '.', '.', '.', '.', 'v', '.', ' '], # 4
        [' ', '.', '.', '.', '.', '.', '.', '.', '.', '.', ' '], # 5
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '.', ' ']  # 6
    ]

    board = Board(grid, [])

    # check the start
    assert board.adj(0, 1) == {(1, 1)}

    # check the four corners
    assert board.adj(1, 1, coming_back=True) == {(1, 2), (2, 1), (0, 1)}
    assert board.adj(1, 9) == {(1, 8), (2, 9)}
    assert board.adj(5, 1) == {(5, 2), (4, 1)}
    assert board.adj(5, 9) == {(4, 9), (5, 8), (6, 9)}

    # check the four inner edges
    assert board.adj(1, 5) == {(1, 6), (2, 5), (1, 4)}
    assert board.adj(3, 9) == {(4, 9), (3, 8), (2, 9)}
    assert board.adj(5, 5) == {(5, 6), (5, 4), (4, 5)}
    assert board.adj(3, 1) == {(3, 2), (4, 1), (2, 1)}

    # check somewhere in the middle
    assert board.adj(3, 5) == {(3, 6), (4, 5), (3, 4), (2, 5)}

    # check for destination
    assert board.adj(5, 9) == {(6, 9), (5, 8), (4, 9)}
    assert board.adj(6, 9) == {(5, 9)}


if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv
    p1 = '-p1' in sys.argv
    p2 = '-p2' in sys.argv
    tests = '-tests' in sys.argv
    grid, blizzards = parse_input(sample)
    if p1:
        board = Board(grid, blizzards)
        part1(board, verbose)
        pass
    elif p2:
        board = Board(grid, blizzards)
        part2(board, verbose)
    elif tests:
        blizzard_tests()
        neighbour_tests()