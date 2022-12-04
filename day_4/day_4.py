lines = open('input.txt').read().splitlines()
# print(lines)
# print(len(lines))

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

# print(assignments)



def part_1():
    overlaps = 0
    for assignment in assignments:
        first, second = assignment
        if set(first) <= set(second) or set(second) <= set(first):
            overlaps += 1
    print(overlaps)


def part_2():
    overlaps = 0
    for assignment in assignments:
        first, second = assignment
        if (set(first) & set(second)) or (set(second) & set(first)):
            overlaps += 1
    
    print(overlaps)

part_2()
