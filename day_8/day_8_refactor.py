import sys
import functools

def parse_input(sample=False, verbose=False):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'
    
    with open(filename) as f:
        grid = [list(map(int, list(i))) for i in [x.rstrip('\n') for x in f.readlines()]]
    
    if verbose:
        print(grid)
    
    return grid


def next_tree(start, direction, grid, verbose=False):
    row, column = start
    height = len(grid)
    width = len(grid[0])
    
    current_tree = grid[row][column]

    dx, dy = direction
    rdx = row
    cdy = column

    if verbose:
        print(f'current tree: ({row}, {column}) {str(current_tree)}')

    while (0 < rdx < height - 1 and 0 < cdy < width - 1):
        rdx += dx
        cdy += dy
        other_tree = grid[rdx][cdy]
        yield other_tree


def explore(grid, verbose=False):
    height = len(grid)
    width = len(grid[0])
    # left, top, right, bottom
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    visibles = 0
    max_score = 0
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            current_tree = grid[i][j]
            visibilities = []
            scores = []
            # pick a direction and determine its visibility and score
            for d in directions:
                score = 0
                visible = True
                # assume we are visible untill we get blocked
                for other_tree in next_tree((i, j), d, grid, verbose):
                    score += 1
                    if current_tree <= other_tree:
                        visible = False
                        break
                visibilities.append(visible)
                scores.append(score)
                
            current_score = functools.reduce(lambda a, b: a*b, scores)
            if current_score > max_score:
                max_score = current_score

            if any(visibilities):
                visibles += 1

    edges = (height * 2) + (width * 2) - 4
    print(f'visibles: {visibles + edges}')
    print(f'highest scenic score: {max_score}')


if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv

    forest = parse_input(sample, verbose)
    explore(forest, verbose)