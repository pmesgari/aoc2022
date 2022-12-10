import sys



def execute(instructions):
    history = []
    start_cycle = 1
    end_cycle = 2
    X = 1
    to_update = False
    for index, instr in enumerate(instructions):
        ops_code, arg = instr
        if to_update:
            # grab the last value of X
            _, to_add, _, _, _ = history[-1]
            X = X + to_add
            to_update = False
        if ops_code == 'noop':
            history.append((ops_code, arg, start_cycle, end_cycle, X))
            start_cycle = end_cycle
            end_cycle = start_cycle + 1
        
        elif ops_code == 'addx':
            tick_1 = (ops_code, arg, start_cycle, end_cycle, X)
            start_cycle = end_cycle
            end_cycle = start_cycle + 1
            tick_2 = (ops_code, arg, start_cycle, end_cycle, X)
            start_cycle = end_cycle
            end_cycle = start_cycle + 1
            history.append(tick_1)
            history.append(tick_2)
            to_update = True
            if index == len(instructions) - 1:
                X = X + arg
    # print(history)
    signals = [
        history[19][-1] * 20,
        history[59][-1] * 60, 
        history[99][-1] * 100,
        history[139][-1] * 140,
        history[179][-1] * 180, 
        history[219][-1] * 220]
    print(sum(signals))
    return history


def draw(history):
    crt = []
    row = ''
    print(len(history))
    for index, h in enumerate(history):
        cycle = index + 1
        _, _, _, _, x = h

        if cycle > 39 and cycle % 40 == 1 or cycle == len(history) - 1:
            crt.append(row)
            row = ''
        if x <= cycle % 40 and cycle % 40 <= x + 2:
            row += '#'
        else:
            row += ' '
    
    print('\n'.join(crt))
        



if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv
    filename = 'input.txt'
    
    if sample:
        filename = 'sample.txt'
    with open(filename) as f:
        lines = [line.split(' ') for line in f.read().splitlines()]
    
    instructions =  list(map(lambda x: (x[0], int(x[1]) if len(x) == 2 else ''), lines))
    # instructions = [('noop', ''), ('addx', 3), ('addx', -5)]
    # print(instructions)

    history = execute(instructions)
    draw(history)