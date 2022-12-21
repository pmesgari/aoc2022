import sys


def parse_input(sample):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines
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

def part1(numbers):
    def adjust(numbers):
        mixed = numbers.copy()
        for idx, num in numbers:
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
        
    # 1, 2, -3, 4, 0, 3, -2
    print(adjust(numbers))
    pretty_print(adjust(numbers))
    

def part2(numbers):
    pass


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