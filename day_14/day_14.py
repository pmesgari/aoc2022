import sys
import math


def parse_input_sample():
    return [
        ['.', '.', '.', '.', '.', '.', '+', '.', '.', '.'], # 0
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], # 1
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], # 2
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], # 3
        ['.', '.', '.', '.', '#', '.', '.', '.', '#', '#'], # 4
        ['.', '.', '.', '.', '#', '.', '.', '.', '#', '.'], # 5
        ['.', '.', '#', '#', '#', '.', '.', '.', '#', '.'], # 6
        ['.', '.', '.', '.', '.', '.', '.', '.', '#', '.'], # 7
        ['.', '.', '.', '.', '.', '.', '.', '.', '#', '.'], # 8
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', '.'], # 9
    ]


def parse_input(sample, verbose):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'

    with open(filename) as f:
        lines = [line.split(' -> ') for line in f.read().splitlines()]
    
    line_tuples = []
    for l in lines:
        l_tuple = []
        for p in l:
            col, row = p.split(',')
            l_tuple.append((int(row), int(col)))
        line_tuples.append(l_tuple)
    
    rows = []
    cols = []
    for l in line_tuples:
        for p in l:
            row, col = p
            rows.append(int(row))
            cols.append(int(col))
    print(f'({min(rows)}, {max(rows)}), ({min(cols)}, {max(cols)})')
    print(f'grid size: rows={max(rows)} columns={max(cols) - min(cols)}')
    sand_source = (0, 500 - min(cols))
    print(f'sand source: {sand_source}')

    MAX_ROWS = max(rows)
    MAX_COLUMN = max(cols)
    MIN_COLUMN = min(cols)

    adjusted_lines = []
    for line in line_tuples:
        l_tuple = []
        for p in line:
            row, col = p
            l_tuple.append((row, col - MIN_COLUMN))
        adjusted_lines.append(l_tuple)

    grid = []
    for _ in range(MAX_ROWS + 1):
        row = []
        for _ in range(((MAX_COLUMN - MIN_COLUMN) + 1)):
            row.append('.')
        grid.append(row)

    for line in adjusted_lines:
        prev = 0
        cur = 1
        while cur < len(line):
            start = line[prev]
            end = line[cur]
            # same column
            if start[1] == end[1]:
                if end[0] < start[0]:
                    start, end = end, start
                for i in range(start[0], end[0] + 1):
                    grid[i][start[1]] = '#'
            # same row
            elif start[0] == end[0]:
                if end[1] < start[1]:
                    start, end = end, start
                for i in range(start[1], end[1] + 1):
                    grid[start[0]][i] = '#'

            prev = cur
            cur += 1
    
    s_r, s_c = sand_source
    grid[s_r][s_c] = '+'

    return sand_source, MAX_ROWS, grid

def get_point(p, grid):
    row, col = p
    return grid[row][col]


def print_grid(grid):
    for r in grid:
        print(''.join(r))

def expand_grid(grid):
    factor = (len(grid[0]) // 2) * 10
    expanded_grid = []
    for line in grid:
        e_l = ['.'] * factor + line + ['.'] * factor
        expanded_grid.append(e_l)

    sand_source = None
    for i in range(len(expanded_grid)):
        for j in range(len(expanded_grid[0])):
            if expanded_grid[i][j] == '+':
                sand_source = (i, j)
    return sand_source, expanded_grid
    

def fall(start, grid, verbose=False):
    row, col = start
    BOTTOM = len(grid) - 2
    while row <= BOTTOM:
        p1 = (row + 1, col)
        p2 = (row + 1, col - 1)
        p3 = (row + 1, col + 1)
        if get_point(p1, grid) not in ['#', 'o']:
            row += 1
        elif get_point(p2, grid) not in ['#', 'o']:
            row += 1
            col -= 1
        elif get_point(p3, grid) not in ['#', 'o']:
            row += 1
            col += 1
        else:
            grid[row][col] = 'o'
            row = BOTTOM + 1
        if verbose:
            print_grid(grid)


def stringify(grid):
    grid_string = ""
    for row in grid:
        grid_string += ''.join(row)
    
    return grid_string


if __name__ == '__main__':
    def simulate(grid, sand_source):
        count = 0
        prev = stringify(grid)
        cur = ""
        while prev != cur:
            prev = cur
            fall(sand_source, grid, verbose)
            cur = stringify(grid)
            count += 1
        return count - 1

    def part_1():
        sand_source, max_rows, grid = parse_input(sample, verbose)
        print(simulate(grid, sand_source))

    def part_2():
        _, _, grid = parse_input(sample, verbose)
        sand_source, expanded_grid = expand_grid(grid)
        
        expanded_grid.append(['.'] * len(expanded_grid[0]))
        expanded_grid.append(['#'] * len(expanded_grid[0]))
        print(simulate(expanded_grid, sand_source))

    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv
    p1 = '-1' in sys.argv
    p2 = '-2' in sys.argv
    if p1:
        part_1()
    elif p2:
        part_2()