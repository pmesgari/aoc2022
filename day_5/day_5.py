import sys
import csv


def parse_input(sample=True, verbose=False):
    filename = 'input.txt'
    if sample:
        filename = 'sample.txt'
    
    cargo, instructions = open(filename).read().split('\n\n')
    
    n = 4
    chunks = []
    for c in cargo.splitlines():
        chunks.append([s.replace(" ", "") for s in [c[i:i+n] for i in range(0, len(c), n)]])
    
    stacks = {}
    for _, c in enumerate(chunks[:-1]):
        # print(c)
        for index, item in enumerate(c):
            if str(index + 1) not in stacks:
                stacks[str(index + 1)] = []
            if item:
                stacks[str(index + 1)].append(item)

    moves = []
    for line in instructions.split('\n'):
        print(line)
        parts = line.split(' ')
        print(parts)
        quantity = parts[1]
        source = parts[3]
        destination = parts[-1]
        moves.append((quantity, source, destination))

    # print(moves)

    return stacks, moves


def make_one_move(move, stacks):
    _, source, destination = move
    item_to_move = stacks[source][0]
    stacks[destination].insert(0, item_to_move)
    stacks[source] = stacks[source][1:]


def part_1(stacks, moves):
    for move in moves:
        quantity, _, _ = move
        for _ in range (int(quantity)):
            make_one_move(move, stacks)
    # print(stacks)
    for key, val in stacks.items():
        print(val[0])


def make_batch_move(move, stacks):
    quantity, source, destination = move
    items_to_move = stacks[source][:int(quantity)]
    print(items_to_move)
    stacks[destination] = items_to_move + stacks[destination]
    stacks[source] = stacks[source][int(quantity):]
    print(stacks)


def part_2(stacks, moves):
    for move in moves:
        quantity, _, _ = move
        make_batch_move(move, stacks)

    for key, val in stacks.items():
        print(val[0])


if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv
    parse_input(sample=sample, verbose=verbose)
    stacks, moves = parse_input(sample=sample, verbose=verbose)
    print(stacks)
    print(moves)

    # part_1(stacks=stacks, moves=moves)
    part_2(stacks=stacks, moves=moves)