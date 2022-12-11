import sys
from collections import defaultdict
import math



def parse_input(sample=False):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'

    with open(filename) as f:
        chunks = f.read().split('\n\n')

    monkey_lines = []
    for ch in chunks:
        monkey_lines.append([line.lstrip() for line in ch.splitlines()])

    items = defaultdict()
    operations = defaultdict()
    test_vals = defaultdict()
    true_cases = defaultdict()
    false_cases = defaultdict()
    for index, ml in enumerate(monkey_lines):
        for line in ml:
            parts = line.split(':')
            if parts[0].startswith('Starting'):
                items[index] = parts[1].replace(' ', '').split(',')
            elif parts[0].startswith('Operation'):
                equation = parts[1].replace(' ', '').split('=')
                operand = equation[1][3]
                arg = equation[1][4:]
                operations[index] = (operand, arg)
            elif parts[0].startswith('Test'):
                test_val = parts[1].split(' ')[-1]
                test_vals[index] = test_val
            elif parts[0].startswith('If true'):
                true_cases[index] = parts[1].split(' ')[-1]
            elif parts[0].startswith('If false'):
                false_cases[index] = parts[1].split(' ')[-1]

    return items, operations, test_vals, true_cases, false_cases


def execute(ops, val):
    operand, arg = ops
    if arg == 'old':
        arg = val
    if operand == '*':
        return int(arg) * val
    if operand == '+':
        return int(arg) + val

def process(items, operations, test_vals, true_cases, false_cases, rounds, part_2=False):
    counts = defaultdict(int)
    lcm = math.lcm(*[int(v) for v in test_vals.values()])
    for _ in range(rounds):
        for key, val in items.items():
            while val:
                item = val.pop(0)
                counts[key] += 1
                # print(key, item, execute(operations[key], int(item)))
                new_val = execute(operations[key], int(item) % lcm if part_2 else int(item))
                if new_val % int(test_vals[key]) == 0:
                    next_monkey = true_cases[key]
                    # print(f'thrown item {new_val} to {next_monkey}')
                    items[int(next_monkey)].append(new_val)
                else:
                    next_monkey = false_cases[key]
                    # print(f'thrown item {new_val} to {next_monkey}')
                    items[int(next_monkey)].append(new_val)

                # print(items)
    
    print(counts)
    sorted_counts = sorted(counts.values(), reverse=True)
    print(sorted_counts[0] * sorted_counts[1])

if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv

    # part 1
    items, operations, test_vals, true_cases, false_cases = parse_input(sample)
    process(items, operations, test_vals, true_cases, false_cases, 20)
    # part 2
    items, operations, test_vals, true_cases, false_cases = parse_input(sample)
    process(items, operations, test_vals, true_cases, false_cases, 10000, True)