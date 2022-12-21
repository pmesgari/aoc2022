import sys
from collections import deque


def parse_input(sample):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'

    with open(filename) as f:
        lines = [tuple(map(int, line.split(',')))
                 for line in f.read().splitlines()]
    cubes = {}
    for line in lines:
        cubes[line] = 6
    return cubes


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
    for cube in cubes:
        for neighbour in adj(cube):
            if neighbour in cubes:
                cubes[cube] -= 1

    total = 0
    for _, val in cubes.items():
        total += val
    print(total)


def part2(cubes):
    max_x = -float('inf')
    max_y = -float('inf')
    max_z = -float('inf')
    min_x = float('inf')
    min_y = float('inf')
    min_z = float('inf')

    for cube in cubes:
        x, y, z = cube
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        max_z = max(max_z, z)
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        min_z = min(min_z, z)

    range_x = range(min_x - 2, max_x + 2)
    range_y = range(min_y - 2, max_y + 2)
    range_z = range(min_z - 2, max_z + 2)

    start = (-1, -1, -1)

    def explore(start):
        touched = 0
        seen = set()
        Q = deque([start])

        while Q:
            item = Q.pop()

            if item in seen:
                continue
            seen.add(item)

            for n in adj(item):
                nx, ny, nz = n
                if nx not in range_x or ny not in range_y or nz not in range_z:
                    continue
                if n in cubes:
                    touched += 1
                    continue
                Q.append(n)

        return touched

    print(explore(start))


if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv
    p1 = '-p1' in sys.argv
    p2 = '-p2' in sys.argv
    inp = parse_input(sample)
    if p1:
        part1(inp)
    elif p2:
        part2(inp)
