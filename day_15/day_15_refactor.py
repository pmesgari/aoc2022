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


def calc_distance(pt1, pt2):
    """
    Calculate the Manhattan distance for two pointss
    """
    x1, y1 = pt1
    x2, y2 = pt2

    return abs(x1 - x2) + abs(y1 - y2)



def intersect(h, sensor, beacon):
    """
    Calculates the most left and right intersection points for a given horizontal line
    """
    x, y = sensor
    r = calc_distance(sensor, beacon)
    left = (x - abs(r - abs(y - h)), h)
    right = (x + abs(r - abs(y - h)), h)

    return left, right


def overlaps(a, b):
    """
    Given two ranges tells if there is an overlap or not
    """
    a1, a2 = a
    b1, b2 = b

    o1 = max(a1, b1)
    o2 = min(a2, b2)

    return o2 >= o1
    

def get_sensor_ranges(h, sensors, beacons):
    """
    For each <sensor, beacon> determine if they intersect h and calculate left and right points if they do
    then disregard the y component, sort the ranges based on x and return them
    """
    ranges = set([])
    for index, s in enumerate(sensors):
        b = beacons[index]
        r = calc_distance(s, b)
        # do we have an intersection?
        min_y = s[1] - r
        max_y = s[1] + r
        if min_y <= h <= max_y:
            left, right = intersect(h, s, b)
            ranges.add((left, right))

    # disregard the y component and make horizontal ranges
    x_ranges = []
    for i in ranges:
        a, b = i
        x_ranges.append((a[0], b[0]))

    # sort the ranges from lowest left to highest left
    sorted_ranges = sorted(x_ranges, key=lambda item: item[0])
    return sorted_ranges


def gaps(ranges):
    result = []
    current = ranges[0]
    for i in range(1, len(ranges)):
        c_start, c_end = current
        r = ranges[i]
        r_start, r_end = r
        if overlaps(current, r):
            if c_end <= r_end:
                current = r
        else:
            for j in range(current[1] + 1, r_start):
                result.append(j)
            current = r
    return result


def part_1(h, sensors, beacons, verbose=False):
    full_ranges = get_sensor_ranges(h, sensors=sensors, beacons=beacons)
    not_covered = gaps(full_ranges)
    if verbose:
        print(full_ranges)
        print(not_covered)
    start = full_ranges[0][0]
    end = full_ranges[-1][1]
    max_range = end - start + 1
    count = max_range
    count -= len(not_covered)
    seen = set([])
    for b in beacons:
        x, y = b
        if y == h and b not in seen:
            count -= 1
            seen.add(b)
    seen = set([])
    for s in sensors:
        x, y = s
        if y == h and s not in seen:
            count -= 1
    print(f'Total count after adjusting for B: {count}')


def part_2(hmin, hmax, sensors, beacons, verbose=False):
    durations_get_sensor_ranges = []
    durations_gaps = []
    for h in range(hmin, hmax + 1):
        full_ranges = get_sensor_ranges(h, sensors=sensors, beacons=beacons)
        not_covered = gaps(full_ranges)
        if verbose:
            print(full_ranges, not_covered)
        if not_covered:
            for nc in not_covered:
                print(nc * 4000000 + h)
                return
    
    print(f'Max duaration: {max(durations_get_sensor_ranges)}, {max(durations_gaps)}')



if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv
    p1 = '-p1' in sys.argv
    p2 = '-p2' in sys.argv

    sensors, beacons = parse_input(sample, verbose)
    if p1:
        if sample:
            hmin = 0
            hmax = 20
        else:
            h = 2000000
        part_1(hmin, hmax, sensors=sensors, beacons=beacons, verbose=verbose)
    elif p2:
        if sample:
            hmin = 0
            hmax = 20
        else:
            hmin = 0
            hmax = 1000000
            # hmin = 3000000
            # hmax = 4000000
        part_2(hmin, hmax, sensors=sensors, beacons=beacons, verbose=verbose)