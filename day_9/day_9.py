import sys


def parse_input(sample=False, verbose=False):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'
    
    with open(filename) as f:
        moves = [item.split(' ') for item in [l.rstrip('\n') for l in f.readlines()]]
        moves = list(map(lambda x: (x[0], int(x[1])), moves))
    
    if verbose:
        print(moves)
    
    return moves


def adj(v):
    x, y = v

    left = (x - 1, y)
    top = (x, y + 1)
    right = (x + 1, y)
    bottom = (x, y - 1)

    # north west
    nw = (x - 1, y + 1)
    # north east
    ne = (x + 1, y + 1)
    # south east
    se = (x + 1, y - 1)
    # south west
    sw = (x - 1, y - 1)

    return [
        left, top, right, bottom,
        nw, ne, se, sw
    ]


def step(start, direction):
    x, y = start

    if direction == 'L':
        return (x - 1, y)
    if direction == 'U':
        return (x, y + 1)
    if direction == 'R':
        return (x + 1, y)
    if direction == 'D':
        return (x, y - 1)
    if direction == 'NW':
        return (x - 1, y + 1)
    if direction == 'NE':
        return (x + 1, y + 1)
    if direction == 'SE':
        return (x + 1, y - 1)
    if direction == 'SW':
        return (x - 1, y - 1)

    
def rel_dir(t, h):
    """
    returns the relative direction of t with respect to h
    """
    x_t, y_t = t
    x_h, y_h = h

    rel_pos = (x_t - x_h, y_t - y_h)
    if rel_pos == (-1, 0):
        return 'L'
    if rel_pos == (0, 1):
        return 'U'
    if rel_pos == (1, 0):
        return 'R'
    if rel_pos == (0, -1):
        return 'D'
    if rel_pos == (-1, 1):
        return 'NW'
    if rel_pos == (1, 1):
        return 'NE'
    if rel_pos == (1, -1):
        return 'SE'
    if rel_pos == (-1, -1):
        return 'SW'


dir_reverse = {
    'L': 'R',
    'U': 'D',
    'R': 'L',
    'D': 'U',
    'NW': 'SE',
    'NE': 'SW',
    'SE': 'NW',
    'SW': 'NE'
}

def part_1(moves, verbose=False):
    h = (0, 0)
    t = (0, 0)

    visited = [h]
    for move in moves:
        direction, quantity = move
        for _ in range(quantity):
            # before we take a step find the relative direction of T with respect to H
            if t == h:
                t_dir = dir_reverse[direction]
            else:
                t_dir = rel_dir(t, h)
            if verbose:
                print(h, t, t_dir)
            h = step(h, direction)
            neighbours = adj(h)
            # if t does not overlap or is not a neighbour anymore
            if t != h and t not in neighbours:
                # find the reverse direction to move T and take a step
                t = step(t, dir_reverse[t_dir])
                if t not in visited:
                    visited.append(t)
    if verbose:
        print(visited)
    print(f'number of visited positions: {len(visited)}')


def move_tail(h, t):
    x_h, y_h = h
    x_t, y_t = t

    dx = x_h - x_t
    dy = y_h - y_t

    # touching either diagonally, horizontally or vertically
    if abs(dx) <= 1 and abs(dy) <= 1:
        return t
    # two steps away        
    if abs(dx) == 2 and abs(dy) == 2:
        # t left of h
        if x_t < x_h:
            x_t_prime = x_t + 1
        # t right of h
        else:
            x_t_prime = x_t - 1

        # t below h
        if y_t < y_h:
            y_t_prime = y_t + 1
        # t above h
        else:
            y_t_prime = y_t - 1
        return (x_t_prime, y_t_prime)

    if abs(dx) == 2 or abs(dy) == 2:
        if abs(dx) == 2:
            if x_t < x_h:
                x_t_prime = x_t + 1
            else:
                x_t_prime = x_t - 1
            y_t = y_h
            return (x_t_prime, y_t)
        elif abs(dy) == 2:
            if y_t < y_h :
                y_t_prime = y_t + 1
            else:
                y_t_prime = y_t - 1
            x_t = x_h
            return (x_t, y_t_prime)


def part_2(moves, verbose=False):
    rope = [(0, 0)] * 10
    visited = [rope[0]]
    for move in moves:
        direction, quantity = move
        for _ in range(quantity):
            # first move the head
            rope[0] = step(rope[0], direction)
            # now move every other part with respect to head
            for i in range(1, len(rope)):
                rope[i] = move_tail(rope[i - 1], rope[i])
            if rope[-1] not in visited:
                visited.append(rope[-1])

    # 3425 wrong
    # 2434
    print(f'nine rope number of visited positions {len(visited)}')


if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv

    # sample_moves = [['R', 4], ['U', 4]]
    # sample_moves = [('R', 5), ('U', 2)]
    instructions = parse_input(sample, verbose)
    part_1(instructions, verbose)
    part_2(instructions, verbose)