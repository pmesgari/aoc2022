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


def calc_boundaries(sensors, beacons):
    xs = []
    ys = []
    for i, s in enumerate(sensors):
        x, y = s
        b = beacons[i]
        r = calc_distance(s, b)
        xs.extend([x - r, x + r])
        ys.extend([y - r, y + r])
    
    max_x = max(xs)
    min_x = min(xs)
    max_y = max(ys)
    min_y = min(ys)

    return max_x, min_x, max_y, min_y



def calc_distance(pt1, pt2):
    """
    Calculate the Manhattan distance for two pointss
    """
    x1, y1 = pt1
    x2, y2 = pt2

    return abs(x1 - x2) + abs(y1 - y2)


def in_range(pt, sensor, beacon):
    """
    Given a point determine if it falls in range of of the sensor
    """
    d = calc_distance(pt, sensor) # manhattan distance from sensor to the point
    r = calc_distance(sensor, beacon) # manhattan distance from sensor to the beacon
    return d <= r


def intersect(h, sensor, beacon):
    x, y = sensor
    r = calc_distance(sensor, beacon)
    left = (x - abs(r - abs(y - h)), h)
    right = (x + abs(r - abs(y - h)), h)

    return left, right


def print_grid(grid):
    for r in grid:
        print(''.join(r))


def get_in_range_sensors(pt, sensors, beacons):
    result = []
    for index, s in enumerate(sensors):
        b = beacons[index]
        if in_range(pt, s, b):
            result.append((s, b))

    return result


def part_1(h, sensors, beacons):
    max_x, min_x, max_y, min_y = calc_boundaries(sensors=sensors, beacons=beacons)
    start = (min_x, h)
    ranges = []
    print(start)
    while start[0] <= max_x:
        for index, s in enumerate(sensors):
            b = beacons[index]
            if in_range(start, s, b):
                left, right = intersect(h, s, b)
                ranges.append((left, right))
                start = (right[0], h)
        else:
            start = (start[0] + 1, h)

    print(ranges)

    xs = []
    for r in ranges:
        start, end = r
        xs.extend([start[0], end[0]])

    count = max(xs) - min(xs) + 1
    seen = set([])
    for b in beacons:
        x, y = b
        if y == h and b not in seen:
            count -= 1
            seen.add(b)
    for s in sensors:
        x, y = s
        if y == h:
            count -= 1
    print(count)



def part_2(h, sensors, beacons):
    def find_point():
        for h_prime in range(h + 1):
            start = (0, h_prime)
            while start[0] <= h:
                for index, s in enumerate(sensors):
                    b = beacons[index]
                    if in_range(start, s, b):
                        left, right = intersect(start[1], s, b)
                        # ranges.append((left, right))
                        start = (right[0], h_prime)
                else:
                    return start
    start = find_point()
    print(start)
    print(start[0] * 4000000 + start[1])

if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv
    p1 = '-p1' in sys.argv
    p2 = '-p2' in sys.argv

    sensors, beacons = parse_input(sample, verbose)
    # print(in_range((0, 0), sensors[0], beacons[0]))
    # print(intersect(2000000 , sensors[0], beacons[0]))
    if p1:
        part_1(2000000, sensors=sensors, beacons=beacons)
    elif p2:
        part_2(4000000, sensors=sensors, beacons=beacons)