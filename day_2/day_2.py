lines = open('input.txt').read().splitlines()
# print(lines)

strategy = [tuple(line.split(' ')) for line in lines]
# print(strategy)

outcomes = {
    ('A', 'X'): 'L',
    ('A', 'Y'): 'D',
    ('A', 'Z'): 'W',
    ('B', 'X'): 'L',
    ('B', 'Y'): 'D',
    ('B', 'Z'): 'W',
    ('C', 'X'): 'L',
    ('C', 'Y'): 'D',
    ('C', 'Z'): 'W',
    ('A', 'D'): 'X',
    ('A', 'W'): 'Y',
    ('A', 'L'): 'Z',
    ('B', 'L'): 'X',
    ('B', 'D'): 'Y',
    ('B', 'W'): 'Z',
    ('C', 'W'): 'X',
    ('C', 'L'): 'Y',
    ('C', 'D'): 'Z'
}

scores = {
    'W': 6,
    'D': 3,
    'L': 0,
    'X': 1,
    'Y': 2,
    'Z': 3
}

total_score = 0
for st in strategy:
    other, me = st
    outcome = outcomes[st]
    total_score = total_score + scores[outcome] + scores[me]

print(total_score)

total_score = 0
for st in strategy:
    other, me = st
    decision = outcomes[st]
    shape = outcomes[(other, decision)]
    print(decision + ' ' + shape)
    total_score = total_score + scores[decision] + scores[shape]

print(total_score)

