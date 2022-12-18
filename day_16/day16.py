import sys
from collections import defaultdict
import heapq

def parse_input(sample, verbose):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'

    with open(filename) as f:
        lines = [line.split('; ') for line in f.read().splitlines()]

    graph = defaultdict()
    rates = defaultdict()
    for line in lines:
        left = line[0].split(' ')
        right = line[1].split(' ')
        graph[left[1]] = []
        for r in right:
            if r in ['tunnel', 'tunnels', 'lead', 'leads', 'to', 'valve', 'valves']:
                continue
            graph[left[1]].append(r.lstrip().replace(',', ''))
        rates[left[1]] = int(left[-1].split('=')[-1])

    vertices = []
    for key, value in graph.items():
        if key not in vertices:
            vertices.append(key)
            for v in value:
                if v not in vertices:
                    vertices.append(v)
    return graph, vertices, rates


def dijkstra(s, graph, vertices):
    D = {}
    PI = {}
    Q = []
    S = set()
    
    def init():
        for vertex in vertices:
            D[vertex] = float('inf')
            PI[vertex] = None
        D[s] = 0
    init()

    heapq.heappush(Q, (0, s))

    while Q:
        _, u = heapq.heappop(Q)
        S.add(u)
        if u not in graph:
            adj = []
        else:
            adj = graph[u]
        for v in adj:
            if D[v] > D[u] + 1:
                D[v] = D[u] + 1
                PI[v] = u
                heapq.heappush(Q, (D[v], v))
    return D


def generate_all_paths(shortest_paths, rates, time_limit):
    current_path = []
    all_paths = []
    previous = 'AA'

    nonzero_rates = []
    for v, rate in rates.items():
        if rate != 0:
            nonzero_rates.append(v)

    opened = {}
    for v in nonzero_rates:
        opened[v] = False

    def dfs(previous, current, time):
        time = time - shortest_paths[previous][current] - 1
        current_path.append((current, time))
        opened[current] = True
        for nxt in nonzero_rates:
            # ensure we are never exploring current again
            # ensure we are never exploring an already open valve
            if nxt != current and not opened[nxt]:
                # if we already know going to the next valve means we are out of time
                # then skip, it is not worth it to get there
                if time - shortest_paths[current][nxt] - 1 < 2:
                    continue
                dfs(previous=current, current=nxt, time=time)
        all_paths.append([item for item in current_path])
        current_path.pop(-1)
        opened[current] = False
    
    for v in nonzero_rates:
        dfs(previous, v, time_limit)
    return all_paths


def calc_total_pressure(rates, path):
    result = 0
    for p in path:
        valve, time = p
        result += rates[valve] * time
    return result


def part_1(graph, vertices, rates):
    shortest_paths = defaultdict()
    for key, _ in graph.items():
        shortest_paths[key] = dijkstra(key, graph, vertices)

    all_paths = generate_all_paths(shortest_paths, rates, 30)
    best = 0
    last_p = None
    for p in all_paths:
        total_pressure = calc_total_pressure(rates, p)
        if total_pressure > best:
            best = total_pressure
            last_p = p
    print(last_p)
    print(best)


def part_2(graph, vertices, rates):
    shortest_paths = defaultdict()
    for key, _ in graph.items():
        shortest_paths[key] = dijkstra(key, graph, vertices)

    # generate all possible paths with a time limit of 26 minutes
    all_paths = generate_all_paths(shortest_paths, rates, 26)
    print(len(all_paths))
    # for each path calculate the total pressure released
    total_pressure_releases = defaultdict(int)
    for p in all_paths:
        # make a tuple consisting of the valves
        # we do not care in which order the valves are opened
        combo = frozenset(map(lambda item: item[0], p))
        total_pressure = calc_total_pressure(rates, p)
        if total_pressure > total_pressure_releases[combo]:
            total_pressure_releases[combo] = total_pressure
    
    print(len(total_pressure_releases))

    best = 0
    l1 = None
    l2 = None
    for combo1, tp1 in total_pressure_releases.items():
        for combo2, tp2 in total_pressure_releases.items():
            if len(combo1 & combo2) != 0:
                continue
            total_pressure = tp1 + tp2
            if total_pressure > best:
                l1 = (combo1, tp1)
                l2 = (combo2, tp2)
                best = total_pressure

    print(l1, l2)
    print(best)


if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv
    p1 = '-p1' in sys.argv
    p2 = '-p2' in sys.argv

    graph, vertices, rates = parse_input(sample, verbose)
    if p1:
        part_1(graph, vertices, rates)
    elif p2:
        part_2(graph, vertices, rates)