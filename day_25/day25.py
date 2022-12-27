import sys
from collections import defaultdict


def parse_input(sample):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'

    with open(filename) as f:
        numbers = f.read().splitlines()

    return numbers


snafu_to_decimal = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}

decimal_to_snafu = {

}


def from_snafu(number):
    digits = list(map(lambda d: snafu_to_decimal[d], list(number)))

    value = 0
    for idx, d in enumerate(digits):
        value += 5**(len(digits) - idx - 1) * d

    return value


class DynamicList(list):
    def __getitem__(self, index):
        if index == len(self):
            return 0
        else:
            return super().__getitem__(index)

    def __setitem__(self, index, item):
        if index == len(self):
            self.append(item)
        else:
            super().__setitem__(index, item)


def to_snafu(number):
    s = ""
    while number:
        s += str(number % 5)
        number = number // 5

    snafu_parts = DynamicList(map(int, s))
    for idx, digit in enumerate(snafu_parts):
        if digit == 3:
            snafu_parts[idx + 1] += 1
            snafu_parts[idx] = -2
        elif digit == 4:
            snafu_parts[idx + 1] += 1
            snafu_parts[idx] = -1
        elif digit == 5:
            snafu_parts[idx + 1] += 1
            snafu_parts[idx] = 0
        else:
            snafu_parts[idx] = digit
    snafu = ""
    for val in snafu_parts[::-1]:
        if val == -1:
            snafu += "-"
        elif val == -2:
            snafu += '='
        else:
            snafu += str(val)

    return snafu


assert from_snafu('2=') == 8
assert from_snafu('2=-01') == 976
assert to_snafu(8) == '2='
assert to_snafu(976) == '2=-01'
assert to_snafu(12345) == '1-0---0'
assert to_snafu(314159265) == '1121-1110-1=0'


def solve(inp):
    result = 0
    for number in inp:
        result += from_snafu(number)

    snafu = to_snafu(result)
    print(result)
    print(snafu)


if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv
    inp = parse_input(sample)
    solve(inp)
