import sys
from collections import defaultdict


class Node:
    def __init__(self, label, type_id, val=None, left=None, right=None) -> None:
        self.label = label
        self.val = val
        self.type_id = type_id
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f'Node {self.label}'


def evaluate(node):
    if node.type_id == type_ids['value']:
        return node.val
    else:
        left = evaluate(node.left)
        right = evaluate(node.right)
        return ops[node.type_id](left, right)


def pretty_print(node, spacing=""):
    if node.type_id == type_ids['value']:
        print(f'{spacing}{node.label}: {node.val}')
        return
    else:
        print(f'{spacing}{node.label} {type_ids[node.type_id]}')
        pretty_print(node.left, spacing + " ")
        pretty_print(node.right, spacing + " ")


type_ids = {
    'value': 0,
    '+': 1,
    '*': 2,
    '-': 3,
    '/': 4,
    '=': 5,
    1: '+',
    2: '*',
    3: '-',
    4: '/',
    5: '='
}

ops = {
    1: lambda a, b: a + b,
    2: lambda a, b: a * b,
    3: lambda a, b: a - b,
    4: lambda a, b: a // b
}


solve_ops = {
    1: lambda node, result, left: result - evaluate(node.left) if left else result - evaluate(node.right),
    2: lambda node, result, left: result // evaluate(node.left) if left else result // evaluate(node.right),
    3: lambda node, result, left: evaluate(node.left) - result if left else result + evaluate(node.right),
    4: lambda node, result, left: evaluate(node.left) // result if left else result * evaluate(node.right),
    5: lambda node, result, left: evaluate(node.right) if left else evaluate(node.right)
}


def solve(node, result, unknowns):
    if node is None:
        return result
    if node.type_id == type_ids['value']:
        return result
    else:
        left = True
        if node.left.label in unknowns:
            left = None

        result = solve_ops[node.type_id](node, result, left)
        if left == None:
            return solve(node.left, result, unknowns)
        else:
            return solve(node.right, result, unknowns)


def find_parent(nodes, key):
    root = nodes['root']
    path = []

    def traverse(current, path, key):
        if current is None:
            return False

        path.append(current.label)

        if current.label == key:
            return True

        if traverse(current.left, path, key) or traverse(current.right, path, key):
            return True

        path.pop(-1)
        return False

    traverse(root, path, key)
    return path


b = Node('b', type_ids['value'], None)
c = Node('c', type_ids['value'], 7)
a = Node('a', type_ids['+'], left=b, right=c)
d = Node('d', type_ids['value'], 10)
root = Node('root', type_ids['='], left=a, right=d)

# print(solve(root, None))
# print(find_parent(root, 'd'))


# b = Node('b', 1, type_ids['value'], None, None)
# d = Node('d', 2, type_ids['value'], None, None)
# e = Node('e', 2, type_ids['value'], None, None)
# c = Node('c', 2, type_ids['+'], d, e)
# a = Node('a', None, type_ids['+'], b, c)
# print(evaluate(a))
# pretty_print(a)


def make_a_tree(lines, part2=False):
    nodes = defaultdict()

    def make_a_node(label, value):
        if len(value) == 1:
            if part2 and label == 'humn':
                val = None
            else:
                val = int(value[0])
            node = Node(
                label=label, type_id=type_ids['value'], val=val)
            nodes[label] = node
        elif len(value) == 3:
            left, op, right = value
            node = Node(label=label, type_id=type_ids[op])
            node.left = make_a_node(left, lines[left])
            node.right = make_a_node(right, lines[right])
            nodes[label] = node
        return node
    for label, value in lines.items():
        make_a_node(label, value)

    # pretty_print(nodes['root'])
    return nodes


def parse_input(sample, part2=False):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'
    with open(filename) as f:
        inp = f.read().splitlines()
    lines = defaultdict()
    for line in inp:
        label, job = line.split(': ')
        job_split = job.split(' ')
        lines[label] = job_split
    return make_a_tree(lines, part2)


def part1(nodes):
    print(evaluate(nodes['root']))


def part2(nodes):
    nodes['root'].type_id = type_ids['=']
    unknowns = find_parent(nodes, 'humn')
    print(solve(nodes['root'], None, unknowns=unknowns))


if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv
    p1 = '-p1' in sys.argv
    p2 = '-p2' in sys.argv
    if p1:
        inp = parse_input(sample)
        part1(inp)
    elif p2:
        inp = parse_input(sample, True)
        part2(inp)
