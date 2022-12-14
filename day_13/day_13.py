import sys
import json
from functools import cmp_to_key


def parse_input(sample=False, verbose=False):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'

    with open(filename) as f:
        chunks = [
            [line.lstrip() for line in ch.splitlines()]
            for ch in f.read().split('\n\n')
        ]
    result = []
    for ch in chunks:
        left = json.loads(ch[0].replace("'", "\""))
        right = json.loads(ch[1].replace("'", "\""))
        result.append((left, right))

    if verbose:
        print(result)

    return result


def is_valid(left, right):
    if type(left) == int and type(right) == int:
        if left < right:
            return -1
        elif left == right:
            return 0
        else:
            return 1
    if type(left) != type(right):
        if type(left) != int:
            return is_valid(left, [right])
        elif type(right) != int:
            return is_valid([left], right)
    if type(left) == list and type(right) == list:
        res = []
        min_l = min(len(left), len(right))
        for i in range(min_l):
            r = is_valid(left[i], right[i])
            if r == -1:
                return -1
            elif r == 1:
                return 1
            else:
                res.append(r)

        if len(res) == len(left) and len(left) < len(right):
            return -1
        elif len(res) == len(right) and len(right) < len(left):
            return 1
        else:
            return 0
    
            

# print(is_valid([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]))
# print(is_valid([9], [[8, 7, 6]]))
# print(is_valid([[4,4],4,4], [[4,4],4,4,4]))


def compare(inp, verbose=False):
    ro_count = 0
    ro_items = []
    for index, item in enumerate(inp):
        left, right = item
        if is_valid(left, right) < 0:
            ro_count += 1
            ro_items.append(index + 1)
    
    # 6520 wrong
    print(f'count of right order packets: {ro_count}')
    print(f'sum of the right order packet indices: {sum(ro_items)}')
    if verbose:
        print(ro_items)



if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv

    inp = parse_input(sample, verbose)
    compare(inp, verbose)
    inp.extend([([[2]], [[6]])])

    part_2_inp = []
    for item in inp:
        left, right = item
        part_2_inp.extend([left, right])
    sorted_inp = sorted(part_2_inp, key=cmp_to_key(is_valid))
    distress_signal = []
    for index, item in enumerate(sorted_inp):
        if item == [[2]] or item == [[6]]:
            distress_signal.append(index + 1)
    print(f'distress signal: {distress_signal[0] * distress_signal[1]}')
