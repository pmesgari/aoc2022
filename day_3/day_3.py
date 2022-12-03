import string


lines = open('input.txt').read().splitlines()
print(lines)
print(len(lines))


def part_1():
    score = 0
    for line in lines:
        first = line[:int(len(line) / 2)]
        second = line[int(len(line) / 2):]
        intersection = next(iter(set(first).intersection(second)))
        if intersection.islower():
            # print(intersection, string.ascii_lowercase.index(intersection) + 1)
            score += string.ascii_lowercase.index(intersection) + 1
        else:
            # print(intersection, string.ascii_uppercase.index(intersection) + 27)
            score += string.ascii_uppercase.index(intersection) + 27

    print(score)


def part_2():
    groups = []
    current = 0
    while current < len(lines):
        # print(current, current + 1, current + 2)
        first = lines[current]
        second = lines[current + 1]
        third = lines[current + 2]
        current = current + 3
        groups.append([first, second, third])

    # print(groups)
    score = 0
    for group in groups:
        intersection =next(iter( set(group[0]) & set(group[1]) & set(group[2])))
        if intersection.islower():
            # print(intersection, string.ascii_lowercase.index(intersection) + 1)
            score += string.ascii_lowercase.index(intersection) + 1
        else:
            # print(intersection, string.ascii_uppercase.index(intersection) + 27)
            score += string.ascii_uppercase.index(intersection) + 27

    print(score)
part_2()