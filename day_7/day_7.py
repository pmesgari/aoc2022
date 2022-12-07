import sys


def parse_input(sample=True, verbose=False):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'
    
    lines = open(filename).read().splitlines()
    path = []
    tree = {}
    for line in lines:
        if line.startswith('$'):
            command = line[2:].split(' ')
            if len(command) == 2:
                if command[-1] == '..':
                    path.pop()
                else:
                    path.append(command[-1])
                continue
            else:
                continue
        key = ''.join(path)
        if key not in tree:
            tree[key] = []
        parts = line.split(' ')
        if parts[0] == 'dir':
            tree[key].append((parts[1], '-'))
        else:
            size, name = parts
            tree[key].append((name, size))
    # print(json.dumps(tree))
    print(tree)
    return tree


def calc_size(path, content, tree):
    size = 0
    for c in content:
        if c[1] == '-':
            size = size + calc_size(path + c[0], tree[path + c[0]], tree)
        else:
            size = size + int(c[1])
    return size


def part_1(tree):
    sizes = []
    for key, value in tree.items():
        print(key, value)
        size = calc_size(key, value, tree)
        sizes.append((key, size))

    wanted = []
    for s in sizes:
        _, value = s
        if value <= 100000:
            wanted.append(value)

    print(sizes)
    print(sum(wanted))

    return sizes


def part_2(sizes):
    total_disk_space = 70000000
    required_free_space = 30000000

    _, current_used_space = sizes[0]
    current_free_space = total_disk_space - current_used_space
    sorted_sizes = sorted(sizes, key=lambda x: x[1])
    for s in sorted_sizes:
        _, value = s
        if current_free_space + value >= required_free_space:
            print(value)
            break


if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv
    tree = parse_input(sample=sample, verbose=verbose)
    sizes = part_1(tree)
    part_2(sizes)
    