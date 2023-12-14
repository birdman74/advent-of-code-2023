import os

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day14.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)

ROLLER = 'O'
BLOCKER = '#'


def day_14():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    lines = data_file.read().split('\n')

    total_load = 0

    for i in range(len(lines[0])):
        col = column(lines, i)
        max_load = len(lines)
        load_for_next_stone = max_load
        for j in range(len(col)):
            c = col[j]
            if c == ROLLER:
                total_load += load_for_next_stone
                load_for_next_stone -= 1
            elif c == BLOCKER:
                load_for_next_stone = max_load - j - 1

    print(f'Total load: {total_load}\n############################\n')


def column(field, index):
    return [line[index] for line in field]


day_14()
