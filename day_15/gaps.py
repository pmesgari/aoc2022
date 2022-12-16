def overlaps(a, b):
    """
    Given two ranges tells if there is an overlap or not
    """
    a1, a2 = a
    b1, b2 = b

    o1 = max(a1, b1)
    o2 = min(a2, b2)

    return o2 >= o1

def full_overlap(a, b):
    a1, a2 = a
    b1, b2 = b

    o1 = max(a1, b1)
    o2 = min(a2, b2)

    return o1 == a1 and o2 == a2 or o1 == b1 and o2 == b2


"""
[(-3, 3), (2, 2), (3, 13), (11, 13), (15, 17), (15, 25)]

current     next    current[1] >= next[0]   current[1]
-3, 3       2, 2    

"""


def gaps(ranges):
    result = []
    current = ranges[0]
    for i in range(1, len(ranges)):
        c_start, c_end = current
        r = ranges[i]
        r_start, r_end = r
        if overlaps(current, r):
            if c_end <= r_end:
                current = r
        else:
            for j in range(current[1] + 1, r_start):
                result.append(j)
            current = r
    return result

print(gaps([(-3, 3), (2, 2), (3, 13), (11, 13), (15, 17), (15, 25)]))
print(gaps([(-986112, 1146470), (53374, 1037438), (657076, 2013646), (1527996, 2493840), (2488746, 3124600), (2729358, 3614264), (3227934, 3244598), (3401432, 3644550), (3614264, 3855672), (3644550, 3993028), (3788690, 4171316)]))

def gaps_(ranges):
    to_remove = []
    for i, r in enumerate(ranges):
        start, end = r
        if start == end:
            # is there a left neighbour
            if i - 1 >= 0:
                if overlaps(ranges[i - 1], r):
                    to_remove.append(r)
            # is there a right neighbour
            elif i + 1 < len(ranges):
                if overlaps(ranges[i + 1], r):
                    to_remove.append(r)
        else:
            # is there a left neighbour
            # (2729358, 3614264), (3227934, 3244598)
            if i - 1 >= 0:
                if full_overlap(ranges[i - 1], r):
                    a1, a2 = r
                    b1, b2 = ranges[i -1]
                    if (max(a1, b1), min(a2, b2)) not in to_remove:
                        to_remove.append((max(a1, b1), min(a2, b2)))
            # is there a right neighbour
            elif i + 1 < len(ranges):
                if full_overlap(ranges[i + 1], r):
                    a1, a2 = r
                    b1, b2 = ranges[i + 1]
                    if (max(a1, b1), min(a2, b2)) not in to_remove:
                        to_remove.append((max(a1, b1), min(a2, b2)))
