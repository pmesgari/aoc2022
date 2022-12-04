import sys
"""
Determining overlaps via ranges without conversion to set

r1:     ----------
r2:  --------

r1:     ----------
r2: ----

r1: --------
r2:     ----------

r1: --------
r2:         ------

r1: --------
r2: --------------

r1:     -----
r2: --------------

r1:         ------
r2: --------------

"""


def parse_input(sample=True, verbose=False):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'
    lines = open(filename).read().splitlines()
    if verbose:
        print(lines)
        print(len(lines))

    lines = [line.split(',') for line in lines]
    assignments = []
    for line in lines:
        sections = []
        first, second = line
        def make_section(r):
            start, end = r.split('-')
            res = [i for i in range(int(start), int(end) + 1)]
            return res
        sections.append(make_section(first))
        sections.append(make_section(second))
        assignments.append(sections)

    return assignments

def part_1(assignments, verbose=False):
    overlaps = 0
    for assignment in assignments:
        first, second = assignment
        if full_overlap(first, second):
            overlaps += 1

    print(f'part 1 answer: {overlaps}')

def right_overlap(r1, r2):
    r11, r12 = r1[0], r1[-1]
    r21, r22 = r2[0], r2[-1]
    if r21 <= r11 <= r22:
        return True
    elif r11 <= r21 <= r12:
        return True
    return False


def left_overlap(r1, r2):
    r11, r12 = r1[0], r1[-1]
    r21, r22 = r2[0], r2[-1]
    if r21<= r12 <= r22:
        return True
    elif r11 <= r22 <= r12:
        return True
    return False

def full_overlap(r1, r2):
    r11, r12 = r1[0], r1[-1]
    r21, r22 = r2[0], r2[-1]
    if r11 >= r21 and r12 <= r22:
        return True
    elif r21 >= r11 and r22 <= r12:
        return True
    return False


def part_2(assignments, verbose=False):
    overlaps = 0
    for assignment in assignments:
        first, second = assignment

        if right_overlap(first, second):
            overlaps += 1
        elif left_overlap(first, second):
            overlaps += 1
    print(f'part 2 answer: {overlaps}')

def part_1_use_set(assignments, verbose=False):
    print('using sets')
    overlaps = 0
    for assignment in assignments:
        first, second = assignment
        if set(first) <= set(second) or set(second) <= set(first):
            overlaps += 1
    print(f'part 1 answer: {overlaps}')


def part_2_use_set(assignments, verbose=False):
    print('using sets')
    overlaps = 0
    for assignment in assignments:
        first, second = assignment
        if (set(first) & set(second)) or (set(second) & set(first)):
            overlaps += 1
    
    print(f'part 2 answer: {overlaps}')


if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv
    use_sets = '-use_set' in sys.argv
    assignments = parse_input(sample=sample, verbose=verbose)
    if use_sets:
        part_1_use_set(assignments, verbose)
        part_2_use_set(assignments, verbose)
    else:
        part_1(assignments, verbose)
        part_2(assignments, verbose)