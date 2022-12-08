import sys

def parse_input(sample=False, verbose=False):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'
    
    with open(filename) as f:
        grid = [list(map(int, list(i))) for i in [x.rstrip('\n') for x in f.readlines()]]
    
    if verbose:
        print(grid)
    
    return grid


def explore(grid, verbose=False):
    visible = []
    max_score = 0
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            current_tree = grid[i][j]
            current_row = grid[i]
            current_column = [grid[r][j] for r in range(len(grid))]
            # reverse the left row for part 2
            left_row = current_row[:j][::-1]
            right_row = current_row[j + 1:]
            # reverse the top column for part 2
            top_column = current_column[:i][::-1]
            bottom_column = current_column[i + 1:]

            def calc_score(current_tree, items):
                score = 0
                for item in items:
                    if current_tree > item:
                        score += 1
                    elif current_tree == item:
                        score += 1
                        break
                    elif current_tree < item:
                        score += 1
                        break
                
                return score

            left_score = calc_score(current_tree, left_row)
            right_score = calc_score(current_tree, right_row)
            top_score = calc_score(current_tree, top_column)
            bottom_score = calc_score(current_tree, bottom_column)
            total_score = left_score * right_score * top_score * bottom_score
            if total_score >= max_score:
                max_score = total_score

            if verbose:
                print(current_tree, current_row, current_column,
                        left_row, right_row, top_column, bottom_column,
                        left_score, right_score, top_score, bottom_score
                )
            if current_tree > max(left_row) or current_tree > max(right_row):
                visible.append((i, j))
            elif current_tree > max(top_column) or current_tree > max(bottom_column):
                visible.append((i, j))

    if verbose:
        print(len(grid), len(grid[0]))
        print(visible)

    edges = (len(grid) * 2) + (len(grid[0]) * 2) - 4
    print(len(visible) + edges)
    print(max_score)


if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv

    forest = parse_input(sample, verbose)
    explore(forest, verbose)
