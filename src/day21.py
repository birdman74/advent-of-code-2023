import os

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day21.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)

PLOT = '.'
ROCK = '#'
START = 'S'
STEPS = 64


def day_21():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    garden = data_file.read().split('\n')

    start = ()

    for y in range(len(garden)):
        row = garden[y]
        start_x = row.find(START)
        if start_x > -1:
            start = (start_x, y)
            break

    end_plots = [start]

    for i in range(STEPS):
        new_plots = []
        for plot in end_plots:
            next_steps(plot, garden, new_plots)

        end_plots = list(set(new_plots))

    total_possible_endpoints = len(end_plots)

    print(f'Total possible endpoints: {total_possible_endpoints}\n############################\n')


def next_steps(plot, garden, new_plots):
    x, y = plot

    potential = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

    for p in potential:
        if is_inbounds(p, garden) and is_not_a_rock(p, garden):
            new_plots.append(p)


def is_inbounds(plot, garden):
    x, y = plot
    h = len(garden)
    w = len(garden[0])

    return 0 <= x < w and 0 <= y < h


def is_not_a_rock(p, garden):
    x, y = p
    return garden[y][x] != ROCK


day_21()
