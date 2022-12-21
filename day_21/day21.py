import sys
from collections import defaultdict


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
    1: '+',
    2: '*',
    3: '-',
    4: '/'
}

ops = {
    1: lambda a, b: a + b,
    2: lambda a, b: a * b,
    3: lambda a, b: a - b,
    4: lambda a, b: a // b
}


class Node:
    def __init__(self, label, type_id, val=None, left=None, right=None) -> None:
        self.label = label
        self.val = val
        self.type_id = type_id
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f'Node {self.label}'


class Tree:
    def __init__(self, nodes) -> None:
        self.nodes = nodes


# b = Node('b', 1, type_ids['value'], None, None)
# d = Node('d', 2, type_ids['value'], None, None)
# e = Node('e', 2, type_ids['value'], None, None)
# c = Node('c', 2, type_ids['+'], d, e)
# a = Node('a', None, type_ids['+'], b, c)
# print(evaluate(a))
# pretty_print(a)


def make_a_tree(lines, values, jobs):
    nodes = defaultdict()

    def make_a_node(label, value):
        if len(value) == 1:
            node = Node(
                label=label, type_id=type_ids['value'], val=int(value[0]))
        elif len(value) == 3:
            left, op, right = value
            node = Node(label=label, type_id=type_ids[op])
            node.left = make_a_node(left, lines[left])
            node.right = make_a_node(right, lines[right])
            nodes[label] = node
        return node
    for label, value in lines.items():
        make_a_node(label, value)

    pretty_print(nodes['root'])
    return nodes


def parse_input(sample):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'
    with open(filename) as f:
        inp = f.read().splitlines()
    node_types = defaultdict()
    values = defaultdict()
    jobs = defaultdict()
    lines = defaultdict()
    for line in inp:
        label, job = line.split(': ')
        job_split = job.split(' ')
        lines[label] = job_split
        if len(job_split) == 1:
            node_types[label] = type_ids['value']
            values[label] = job_split[0]
        elif len(job_split) == 3:
            left, op, right = job.split(' ')
            node_types[label] = type_ids[op]
            jobs[label] = (left, op, right)
    return make_a_tree(lines, values, jobs)


def part1(nodes):
    print(evaluate(nodes['pppw']))
    print(evaluate(nodes['sjmn']))


def part2():
    pass


if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv
    p1 = '-p1' in sys.argv
    p2 = '-p2' in sys.argv
    inp = parse_input(sample)
    if p1:
        part1(inp)
    elif p2:
        part2()
