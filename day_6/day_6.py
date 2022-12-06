import sys


def process_datastream(datastream, buffer_size, verbose=False):
    counter = 0
    for i in range(len(datastream)):
        buffer = datastream[i:i+buffer_size]
        counter += 1
        if len(buffer) == buffer_size:
            if verbose:
                print(buffer)
            if len(set(buffer)) == len(buffer):
                print(counter + buffer_size - 1)
                break


def part_1(datastream, buffer_size=4, verbose=False):
    process_datastream(datastream=datastream, buffer_size=buffer_size, verbose=verbose)

def part_2(datastream, buffer_size=14, verbose=False):
    process_datastream(datastream=datastream, buffer_size=buffer_size, verbose=verbose)



if __name__ == '__main__':
    verbose = '-debug' in sys.argv
    sample = '-sample' in sys.argv
    if sample:
        datastream = 'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'
    else:
        datastream = open('input.txt').read()
    
    part_1(datastream=datastream, buffer_size=4)
    part_2(datastream=datastream, buffer_size=14)