import sys


def parse_input(sample):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'

    with open(filename) as f:
        jet_patterns = [1 if jp == '>' else -1 for jp in list(f.readline())]

    return jet_patterns


rocks = [
    [(0, 0), (1, 0), (2, 0), (3, 0)]
]


def print_board(board):
    max_x = 7
    max_y = 7

    grid = [['.'] * max_x for _ in range(max_y + 1)]

    for pt in board:
        x, y = pt
        grid[y][x] = '#'

    for line in grid:
        print(line)
        # print('\n'.join(line))


def play(jet_patterns):
    board = set()
    current_floor = 0

    def allowed(next_pos, board):
        for pt in next_pos:
            x, y = pt
            if y < 1:
                return False
            if (x, y) in board:
                return False
        return True

    def drop(current_pos):
        final_pos = [(x, y) for x, _ in current_pos]
        for pos in final_pos:
            board.add(pos)

    def fall(rock, current_floor):
        floor = current_floor + 4
        i = 0
        dy = -1
        current_pos = [(x + 2, y + floor) for x, y in rock]
        while True:
            dx = jet_patterns[i]
            next_pos = [(x if x + dx > 7 or x + dx < 0 else x + dx, y + dy)
                        for x, y in current_pos]
            if allowed(next_pos, board):
                current_pos = next_pos
                i += 1
            else:
                drop(current_pos)
                break
        current_floor = floor
    fall(rocks[0], current_floor)
    print(board)
    print_board(board)


def part1(jet_patterns):
    play(jet_patterns)


def part2():
    pass


if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv
    p1 = '-p1' in sys.argv
    p2 = '-p2' in sys.argv
    jet_patterns = parse_input(sample)
    if p1:
        part1(jet_patterns)
    elif p2:
        part2()
