import sys
from collections import defaultdict

def parse_input(sample):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'

    with open(filename) as f:
        lines = [tuple(map(int, line.split(','))) for line in f.read().splitlines()]
    
    return lines


def adj(pt):
    x, y, z = pt
    left = (x, y - 1, z)
    top = (x, y, z + 1)
    right = (x, y + 1, z)
    front = (x + 1, y, z)
    back = (x - 1, y, z)
    bottom = (x, y, z - 1)

    return [left, top, right, front, back, bottom]


def part1(cubes):

    counts = {}
    for cube in cubes:
        counts[cube] = 6
    for cube in cubes:
        for neighbour in adj(cube):
            if neighbour in cubes:
                counts[cube] -= 1

    total_sides = len(cubes) * 6
    print(total_sides)
    print(counts)
    total = 0
    for _, val in counts.items():
        total += val
    print(total)

if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv
    p1 = '-p1' in sys.argv
    p2 = '-p2' in sys.argv

    inp = parse_input(sample)
    part1(inp)