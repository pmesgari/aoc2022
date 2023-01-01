import sys
import re
from collections import namedtuple


def parse_input(sample):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'

    with open(filename) as f:
        board, instructions = f.read().split('\n\n')

    lines = board.split('\n')
    max_width = len(max(lines, key=len))
    grid = []
    for line in lines:
        grid.append(list(line) + [' '] * (max_width - len(line)))

    exp = re.compile(r'(\d+)|([LR])')
    moves = []
    for e in exp.findall(instructions):
        moves.append(e)
    
    return grid, moves


DIR = {
    'UP': 'UP',
    'DOWN': 'DOWN',
    'LEFT': 'LEFT',
    'RIGHT': 'RIGHT'
}


DIR_VECTOR = {
    'UP': (-1, 0),
    'DOWN': (1, 0),
    'LEFT': (0, -1),
    'RIGHT': (0, 1)
}

DIR_SCORE = {
    'UP': 3,
    'DOWN': 1,
    'LEFT': 2,
    'RIGHT': 0
}


def turn(t, dir):
    if dir == 'UP':
        return DIR['LEFT'] if t == 'L' else DIR['RIGHT']
    if dir == 'DOWN':
        return DIR['RIGHT'] if t == 'L' else DIR['LEFT']
    if dir == 'LEFT':
        return DIR['DOWN'] if t == 'L' else DIR['UP']
    if dir == 'RIGHT':
        return DIR['UP'] if t == 'L' else DIR['DOWN']
    


def print_path(grid, visited):
    for vis in visited:
        r, c, dir = vis
        if dir == 'UP':
            grid.set_cell(r, c, '^')
        if dir == 'DOWN':
            grid.set_cell(r, c, 'v')
        elif dir == 'LEFT':
            grid.set_cell(r, c, '<')
        elif dir == 'RIGHT':
            grid.set_cell(r, c, '>')
    
    grid.print()


class BaseRowColumn:
    def __init__(self, cells) -> None:
        self.cells = cells

    def get_cells(self, allow_blanks=False):
        result = []
        for cell in self.cells:
            if not allow_blanks and cell == ' ':
                continue
            result.append(cell)
        return result

    @property
    def offset(self):
        cells = self.get_cells(allow_blanks=True)
        count = 0
        for cell in cells:
            if cell != ' ':
                break    
            count += 1

        return count


class Column(BaseRowColumn):
    pass


class Row(BaseRowColumn):
    pass


class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.t_grid = [list(row) for row in zip(*grid)]
        
    def get_column(self, c) -> Column:
        column = Column(self.t_grid[c])
        return column

    def get_row(self, r) -> Row:
        row = Row(self.grid[r])
        return row

    def get_cell(self, r, c):
        return self.grid[r][c]

    def set_cell(self, r, c, value):
        self.grid[r][c] = value

    def print(self):
        for row in self.grid:
            print(''.join(row))


Vector = namedtuple('Vector', 'start magnitude change')


class Board:
    def __init__(self, grid) -> None:
        self.grid = grid
        self.visited = []

    def move(self, instr, position):
        number, letter = instr
        r, c, dir = position
        if number == '':
            self.visited.append((r, c, turn(letter, dir)))
            return r, c, turn(letter, dir)
        else:
            nr, nc = self.teleport(position, int(number))
            self.visited.append((nr, nc, dir))
            return nr, nc, dir

    def step(self, vector: Vector, offset, cells):
        cell = vector.start
        moves = vector.magnitude
        change = vector.change

        cell -= offset

        number = moves
        next_cell = cell
        while number >= 0:
            if cells[next_cell] == '#':
                break
            cell = next_cell
            number -= 1
            next_cell = (cell + change) % (len(cells))
        
        return cell + offset

    def teleport_horizontal(self, row, vector):
        cells = row.get_cells()
        offset = row.offset
        return self.step(vector, offset, cells)


    def teleport_vertical(self, column, vector):
        cells = column.get_cells()
        offset = column.offset
        return self.step(vector, offset, cells)


    def teleport(self, position, number):
        r, c, dir = position
        dr, dc = DIR_VECTOR[dir]

        if dr == 0:
            row = self.grid.get_row(r)
            vector = Vector(c, number, dc)
            nr, nc = r, self.teleport_horizontal(row, vector)
            return nr, nc
        elif dc == 0:
            column = self.grid.get_column(c)
            vector = Vector(r, number, dr)
            nr, nc = self.teleport_vertical(column, vector), c
            return nr, nc


def grid_tests():
    g = [
        # 0 , 1  ,  2 ,  3 ,  4 ,  5 ,  6 ,  7 ,  8 ,  9 , 10
        [' ', ' ', ' ', '.', '.', '.', '.', '.', ' ', ' ', ' '], # 0
        [' ', ' ', ' ', '.', '.', '.', '.', '.', ' ', ' ', ' '], # 1
        [' ', ' ', ' ', '#', '.', '.', '.', '.', ' ', ' ', ' '], # 2
        [' ', ' ', ' ', '.', '.', '.', '.', '#', ' ', ' ', ' '], # 3
        [' ', ' ', ' ', '#', '.', '.', '.', '#', ' ', ' ', ' '], # 4
        [' ', ' ', ' ', '.', '.', '.', '.', '.', ' ', ' ', ' '], # 5
        [' ', ' ', ' ', '.', '.', '.', '.', '.', ' ', ' ', ' ']  # 6
    ]
    grid = Grid(g)
    board = Board(grid)

    assert board.teleport((0, 5, 'RIGHT'), 1) == (0, 6)
    assert board.teleport((0, 5, 'RIGHT'), 2) == (0, 7)
    assert board.teleport((0, 5, 'RIGHT'), 10) == (0, 5)
    assert board.teleport((2, 5, 'RIGHT'), 10) == (2, 7)
    assert board.teleport((2, 5, 'RIGHT'), 10) == (2, 7)
    assert board.teleport((3, 5, 'RIGHT'), 10) == (3, 6)
    assert board.teleport((3, 6, 'RIGHT'), 10) == (3, 6)

    assert board.teleport((0, 5, 'LEFT'), 1) == (0, 4)
    assert board.teleport((0, 5, 'LEFT'), 2) == (0, 3)
    assert board.teleport((0, 5, 'LEFT'), 10) == (0, 5)
    assert board.teleport((2, 5, 'LEFT'), 10) == (2, 4)
    assert board.teleport((2, 5, 'LEFT'), 2) == (2, 4)
    assert board.teleport((3, 5, 'LEFT'), 3) == (3, 3)

    assert board.teleport((0, 4, 'UP'), 1) == (6, 4)
    assert board.teleport((0, 4, 'UP'), 2) == (5, 4)
    assert board.teleport((0, 4, 'UP'), 6) == (1, 4)
    assert board.teleport((1, 3, 'UP'), 1) == (0, 3)
    assert board.teleport((1, 3, 'UP'), 3) == (5, 3)
    assert board.teleport((1, 3, 'UP'), 4) == (5, 3)
    assert board.teleport((3, 3, 'UP'), 3) == (3, 3)

    assert board.teleport((0, 3, 'DOWN'), 1) == (1, 3)
    assert board.teleport((0, 3, 'DOWN'), 2) == (1, 3)
    assert board.teleport((5, 7, 'DOWN'), 1) == (6, 7)
    assert board.teleport((5, 7, 'DOWN'), 2) == (0, 7)
    assert board.teleport((5, 7, 'DOWN'), 4) == (2, 7)



def part1(grid, moves, debug=False):
    c_start = None
    for idx, _ in enumerate(grid.get_row(0).cells):
        if grid.get_cell(0, idx) == '.':
            c_start = idx
            break
    r, c, dir = 0, c_start, DIR['RIGHT']
    board = Board(grid)
    board.visited.append((r, c, dir))
    count = 0
    if debug:
        print(count, None, dir)
        print_path(grid, board.visited)
    for idx, mov in enumerate(moves):
        count += 1
        r, c, dir = board.move(mov, (r, c, dir))
        if debug:
            print(count, mov, dir)
            print_path(grid, board.visited)
        # if count == 3:
        #     break
    print(f'last position: {r}, {c}, {DIR_SCORE[dir]}')
    score = 1000 * (r + 1) + 4 * (c + 1) + DIR_SCORE[dir]
    print(score) 


def part2():
    pass


if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv
    p1 = '-p1' in sys.argv
    p2 = '-p2' in sys.argv
    tests = '-tests' in sys.argv
    g, moves = parse_input(sample)
    if p1:
        grid = Grid(g)
        part1(grid, moves, verbose)
    elif p2:
        part2()
    elif tests:
        grid_tests()