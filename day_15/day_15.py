import sys


def parse_input(sample, verbose):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'

    with open(filename) as f:
        lines = [line.split(': ') for line in f.read().splitlines()]

    sensors = []
    beacons = []
    for line in lines:
        sensor, beacon = line
        s_c = tuple(map(lambda c: int(c.split('=')[-1]), sensor[10:].split(',')))
        b_c = tuple(map(lambda c: int(c.split('=')[-1]), beacon[22:].split(',')))
        sensors.append(s_c)
        beacons.append(b_c)

    return sensors, beacons

def make_grid(sensors, beacons):
    max_x = max(
        max(sensors, key=lambda item: item[0]),
        max(beacons, key=lambda item: item[0])
    )[0]
    max_y = max(
        max(sensors, key=lambda item: item[1]),
        max(beacons, key=lambda item: item[1])
    )[1]
    min_x = min(
        min(sensors, key=lambda item: item[0]),
        min(beacons, key=lambda item: item[0])
    )[0]
    min_y = min(
        min(sensors, key=lambda item: item[1]),
        min(beacons, key=lambda item: item[1])
    )[1]

    print(max_x, min_x, max_y, min_y)

    grid = [['.'] * (max_x - min_x + 1) for _ in range(max_y - min_y + 1)]
    for s in sensors:
        x, y = s
        grid[y - min_y][x - min_x] = 'S'
    for b in beacons:
        x, y = b
        grid[y - min_y][x - min_x] = 'B'
    print_grid(grid)

    return grid, (max_x, min_x, max_y, min_y)


def get_point(p, grid, dim):
    x, y = p
    _, min_x, _, min_y = dim
    return grid[y - min_y][x - min_x]    


def calc_distance(sensor, beacon):
    """
    Calculate the Manhattan distance for a sensor and beacon combo
    """
    x_s, y_s = sensor
    x_b , y_b = beacon

    return abs(x_s - x_b) + abs(y_s - y_b)


def in_range(p, sensors, beacons):
    """
    Given a point determine if it falls in range of any pairs of (sensor, beacon)
    """
    x, y = p
    pairs = list(zip(sensors, beacons))
    for pair in pairs:
        sensor, beacon = pair
        range = calc_distance(sensor, beacon)
        print(pair, range)


def print_grid(grid):
    for r in grid:
        print(''.join(r))


def part_1():
    pass


def part_2():
    pass


if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv
    p1 = '-1' in sys.argv
    p2 = '-2' in sys.argv

    sensors, beacons = parse_input(sample, verbose)
    # grid, dim = make_grid(sensors, beacons)
    # print(get_point((2, 18), grid, dim))
    # print(get_point((-2, 15), grid, dim))
    in_range((0, 0), sensors, beacons)
    if p1:
        part_1()
    elif p2:
        part_2()