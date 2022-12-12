import sys
import heapq


def adj(v, grid):
    row, col = v
    neighbours = []

    right = (row, col + 1)
    left = (row, col - 1)
    top = (row - 1, col)
    bottom = (row + 1, col)

    max_el = grid[row][col] + 1
    for row, col in [right, bottom, left, top]:
        if 0 <= row < len(grid) and 0 <= col < len(grid[row]):
            if grid[row][col] <= max_el:
                neighbours.append((row, col))

    return neighbours


def bfs(s, grid):
    frontiers = [[s]]
    level = {s: 0}
    i = 1
    frontier = [s]
    parent = {s: None, }
    while frontier:
        next = []
        for u in frontier:
            for v in adj(u, grid):
                if v not in level:
                    level[v] = i
                    next.append(v)
                    if v not in parent:
                        parent[v] = u
        frontier = next
        frontiers.append(frontier)
        i += 1

    return level


def dijkstra(s, grid):
    D = {}
    PI = {}
    Q = []
    S = set()

    def init():
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                D[(row, col)] = float('inf')
                PI[(row, col)] = None
        D[s] = 0

    init()

    heapq.heappush(Q, (0, s))

    while Q:
        _, u = heapq.heappop(Q)
        S.add(u)

        for v in adj(u, grid):
            if D[v] > D[u] + 1:
                D[v] = D[u] + 1
                PI[v] = u
                heapq.heappush(Q, (D[v], v))
    return D


"""
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv

    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'

    with open(filename, 'rb') as f:
        grid = []
        target = None
        lines = f.read().splitlines()
        grid = list(map(list, lines))
        a_s = []
        for i, l in enumerate(grid):
            c_l = []
            for j, ch in enumerate(l):
                if ch == ord('E'):
                    target = (i, j)
                    grid[i][j] = ord('z')
                elif ch == ord('S'):
                    source = (i, j)
                    grid[i][j] = ord('a')
                elif ch == ord('a'):
                    a_s.append((i, j))

    min_a = float('inf')
    for a in a_s + [source]:
        sp = dijkstra(a, grid)
        if sp[target] < min_a:
            min_a = sp[target]
    print(a_s)
    print(min_a)
