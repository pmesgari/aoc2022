import sys
from collections import defaultdict
import math



def parse_input(sample=False):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'

    with open(filename) as f:
        chunks = [
            [line.lstrip() for line in ch.splitlines()]
            for ch in f.read().split('\n\n')
        ]

    items = []
    operations = []
    test_vals = []
    true_cases = []
    false_cases = []

    for ch in chunks:
        for line in ch:
            key, val = line.split(':')
            if key.startswith('Starting'):
                items.append(list(map(int, val.split(','))))
            elif key.startswith('Operation'):
                equation = ''.join(val.replace(' ', '').split('=')[1:])
                operator = equation[3]
                a, b = equation.split(operator)
                if operator == '+':
                    operations.append(lambda a, b=b: a + int(b))
                elif operator == '*':
                    if a == b:
                        operations.append(lambda a, b=b: a * a)
                    else:
                        operations.append(lambda a, b=b: a * int(b))
            elif key.startswith('Test'):
                test_vals.append(int(val.split(' ')[-1]))
            elif key.startswith('If true'):
                true_cases.append(int(val.split(' ')[-1]))
            elif key.startswith('If false'):
                false_cases.append(int(val.split(' ')[-1]))

    result = list(zip(items, operations, test_vals, true_cases, false_cases))
    return result


def simulate(monkeys, rounds, part_2=False, verbose=False):
    """
    lcm(a, b, c, d)
    (x + k) % a = ((x % lcm) + k) % a
    """
    counts = defaultdict(int)
    lcm = math.lcm(*[int(v[2]) for v in monkeys])
    for _ in range(rounds):
        for index, m in enumerate(monkeys):
            items, operation, test_val, true_case, false_case = m
            while items:
                item = items.pop(0)
                counts[index] += 1
                if part_2:
                    worry_level = operation(item % lcm)
                else:
                    worry_level = operation(item) // 3
                if worry_level % test_val == 0:
                    other = monkeys[true_case]
                else:
                    other = monkeys[false_case]
                other_items, _, _, _, _ = other
                other_items.append(worry_level)
    if verbose:
        temp = {i: k[0] for i, k in enumerate(monkeys)}
        print(temp)
        print(counts)
    sorted_counts = sorted(counts.values(), reverse=True)
    print(sorted_counts[0] * sorted_counts[1])


if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv
    print('-----------Part 1-----------')
    monkeys = parse_input(sample)
    simulate(monkeys, 20, part_2=False, verbose=verbose)
    print('-----------Part 2-----------')
    monkeys = parse_input(sample)
    simulate(monkeys, 10000, True, verbose=verbose)