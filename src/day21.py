import os
import functools

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day21.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)

PLOT = '.'
ROCK = '#'
START = 'S'
STEPS = 26501365

garden = []
height = 0
width = 0


def day_21():
    # do_stuff()
    do_calculation()


def do_calculation():
    # numbers from do_stuff() discovery with map that has clear
    # vertical & horizontal paths allowing for pattern
    iterations = int((STEPS - 65) / 131)
    steps = 3867
    base_2 = 30386
    iter_growth = 30270

    for i in range(iterations):
        steps += base_2 + (i * iter_growth)

    print(f'Total plot points: {steps}')


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    global garden
    garden = data_file.read().split('\n')
    global height
    height = len(garden)
    global width
    width = len(garden[0])

    start = ()

    for y in range(height):
        row = garden[y]
        start_x = row.find(START)
        if start_x > -1:
            start = (start_x, y)
            break

    total_possible_endpoints = walk_the_garden(start)

    print(f'Total possible endpoints: {total_possible_endpoints}\n############################\n')


def walk_the_garden(start):
    n_minus_one_plots = []
    n_minus_one_count = 0
    end_plots = [start]
    new_total = 1
    leading_edge_about_to_leave = True

    for i in range(STEPS):
        new_plots = take_a_step(end_plots)
        # subtract n-1 plots from new_plots
        new_plots = list(set(new_plots) - set(n_minus_one_plots))

        n_minus_two_count = n_minus_one_count
        n_minus_one_plots = end_plots
        n_minus_one_count = new_total

        new_total = n_minus_two_count + len(new_plots)
        end_plots = new_plots

        # edges on 'S-axis'
        about_to_exit = len([p for p in end_plots if p[0] % width == 0 and p[1] == start[1]]) > 0
        if about_to_exit:
            if leading_edge_about_to_leave:
                print(f'Step: {i}, Total: {new_total}')
            leading_edge_about_to_leave = not leading_edge_about_to_leave

    return new_total


def take_a_step(start_plots):
    new_plots = []

    for plot in start_plots:
        x, y = plot

        x_offset = x // width
        y_offset = y // height

        new_x = x % width
        new_y = y % height

        plots = next_steps((new_x, new_y))
        for x2, y2 in plots:
            new_plots += [(x2 + (width * x_offset), y2 + (height * y_offset))]

    return list(set(new_plots))


@functools.cache
def next_steps(plot):
    x, y = plot
    new_plots = []

    potential = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

    for p in potential:
        x, y = p
        x = x % width
        y = y % height
        if is_not_a_rock((x, y)):
            new_plots.append(p)

    return tuple(new_plots)


def is_inbounds(plot):
    x, y = plot

    return 0 <= x < width and 0 <= y < height


@functools.cache
def is_not_a_rock(p):
    x, y = p

    return garden[y % height][x % width] != ROCK


day_21()
