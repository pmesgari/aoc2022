import sys


def parse_input(sample):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'
    with open(filename) as f:
        lines = f.read().splitlines()
    numbers = []
    for idx, value in enumerate(lines):
        numbers.append((idx, int(value)))

    return numbers


def pretty_print(numbers):
    sorted_numbers = sorted(numbers, key=lambda x: x[0])
    result = []
    for num in sorted_numbers:
        result.append(str(num[1]))
    print(', '.join(result))


def adjust(original, numbers):
    mixed = numbers.copy()
    for idx, _ in original:
        for i, item in enumerate(mixed):
            pos, val = item
            if pos == idx:
                break
        j = (i + val) % (len(mixed) - 1)
        if i < j:
            mixed[i:j] = mixed[i + 1:j + 1]
        elif i > j:
            mixed[j + 1:i + 1] = mixed[j:i]
        mixed[j] = (pos, val)
    return mixed


def calc_grove_coordinates(numbers):
    zero_idx = 0
    for idx, item in enumerate(numbers):
        if item == 0:
            zero_idx = idx

    grove_coordinates = 0
    coordinates = [1000, 2000, 3000]
    for cord in coordinates:
        grove_coordinates += numbers[(zero_idx + cord) %
                                     (len(numbers))]
    print(grove_coordinates)


def part1(numbers):
    result = adjust(numbers, numbers)
    mixed_numbers = [val for _, val in result]
    calc_grove_coordinates(mixed_numbers)


def part2(numbers):
    numbers = [(x[0], x[1] * 811589153) for x in numbers]
    result = numbers
    for _ in range(10):
        result = adjust(numbers, result)

    mixed_numbers = [val for _, val in result]
    calc_grove_coordinates(mixed_numbers)


if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv
    p1 = '-p1' in sys.argv
    p2 = '-p2' in sys.argv

    numbers = parse_input(sample)
    if p1:
        part1(numbers)
    elif p2:
        part2(numbers)
