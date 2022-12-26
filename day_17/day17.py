import sys


def parse_input(sample):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'

    with open(filename) as f:
        jet_patterns = [1 if jp == '>' else -1 for jp in list(f.readline())]

    return jet_patterns


rocks = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (1, 0), (0, 1), (1, 1)]
]

rock_names = {
    0: '----',
    1: '+',
    2: 'L',
    3: 'I',
    4: '#'
}


class Tetris:
    def __init__(self, rocks, jets) -> None:
        self.y_max = 0
        self.width = 7
        self.board = set()
        self.rocks = rocks
        self.jets = jets
        self.current_rock = 0
        self.current_jet = 0

    def print_board(self):
        grid = [
            ['.'] * self.width for _ in range(self.y_max)]
        for pt in self.board:
            x, y = pt
            grid[y - 1][x] = '#'
        new_grid = []
        for i in range(len(grid) - 1, -1, -1):
            new_grid.append(['|'] + grid[i] + ['|'])
        new_grid.append(list('+-------+'))

        print('\n'.join([''.join(line) for line in new_grid]))

    
    def can_move(self, rock, x, y):
        for cell in rock:
            x_c, y_c = cell
            if x_c + x < 0 or x_c + x  >= 7:
                return False
            if y_c + y <= 0:
                return False
            if (x_c + x, y_c + y) in self.board:
                return False
        return True

    def drop(self, rock):
        """
        Instead of starting from row 3 and then applying a jet, its easier to start
        from row 4, do a fall and then apply the jet

        Instead of this:
        |.......| 5
        +-------+
        |..@@@@.| 4
        |.......| 3
        |.......| 2
        |.......| 1 
        +-------+

        We start with this:
        |..@@@@.| 5
        +-------+
        |.......| 4
        |.......| 3
        |.......| 2
        |.......| 1 
        +-------+

        Also, all we need to track during the fall are these two parameters:
            - x coordinate: this is the x coordinate of the left most cell of the rock
            - y coordindate: this is the y coordinate of the bottom most cell of the rock
                the coordinate where the rock appears and the first fall begins
        """
        x = 2
        y = self.y_max + 5
        # can we make one drop?
        while self.can_move(rock, x, y - 1):
            # yes, then drop
            y -= 1
            # can we apply a jet?
            if self.can_move(rock, x + self.jets[self.current_jet], y):
                # yes, then shift left or right
                x += self.jets[self.current_jet]
            self.current_jet = (self.current_jet + 1) % len(self.jets)
        current_cells = [(x_r + x, y_r + y) for x_r, y_r in rock]
        for cell in current_cells:
            self.board.add(cell)
        self.y_max = max(self.y_max, max(y for _, y in current_cells))


    def free(self, x, y):
        return x >= 0 and x < 7 and y > 0 and (x, y) not in self.board


    def ground_shape(self):
        y = 0
        
        visited = set()
        Q = []
        for x in range(7):
            Q.append((x, 0))
        
        while Q:
            x, y = Q.pop()

            if len(visited) > 20:
                break

            if (x, y) in visited:
                continue

            if not self.free(x, self.y_max + y):
                continue
            visited.add((x, y))

            for nx, ny in ((x-1, y), (x+1,y), (x, y-1)):
                Q.append((nx, ny))

        return tuple(visited)  if len(visited) <= 20 else None


    def run(self, count):
        rock = self.rocks[self.current_rock]
        for i in range(count):
            self.drop(rock)
            self.current_rock = (i + 1) % len(self.rocks)
            rock = self.rocks[self.current_rock]



def play(jets, count):
    tetris = Tetris(rocks, jets)
    tetris.run(count)
    # tetris.print_board()
    print(f'tower height is: {tetris.y_max}')


def part1(jets):
    play(jets, 2022)


def part2(jets):
    tetris = Tetris(rocks, jets)
    additional = 0
    cycles = {}
    freqs = []
    count = 1000000000000
    current_count = 0
    for i in range(count):
        if current_count >= count:
            break
        
        rock = tetris.rocks[tetris.current_rock]
        tetris.drop(rock)
        tetris.current_rock = (i + 1) % len(tetris.rocks)
        current_count += 1
        ground = tetris.ground_shape()
        jet = tetris.current_jet
        piece = tetris.current_rock
        if ground is None: continue
        
        if (jet, piece, ground) in cycles:
            oldmaxy, oldcount = cycles[jet, piece, ground]
            frequency = (count - current_count) // (current_count - oldcount)
            growth = (tetris.y_max - oldmaxy)
            additional += growth * frequency
            if frequency != 0:
                current_count = divmod(
                    (count - current_count), 
                    frequency
                )[0] * frequency + current_count
            else:
                continue
            freqs.append([jet, piece, oldcount, frequency, growth, additional])
        cycles[jet, piece, ground] = (tetris.y_max, current_count)
    print(tetris.y_max)
    for f in freqs:
        print(f)
    print(tetris.y_max + additional)


if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv
    p1 = '-p1' in sys.argv
    p2 = '-p2' in sys.argv
    jet_patterns = parse_input(sample)
    if p1:
        part1(jet_patterns)
    elif p2:
        part2(jet_patterns)
