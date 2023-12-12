import os

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day11.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)

SPACE = '.'
GALAXY = '#'
EXPANSION_FACTOR = 1000000


def day_11():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    star_map = data_file.read().split('\n')

    double_rows = []
    double_columns = []

    for y in range(len(star_map)):
        if all(c == SPACE for c in star_map[y]):
            double_rows.append(y)

    for x in range(len(star_map[0])):
        if all(r[x] == SPACE for r in star_map):
            double_columns.append(x)

    galaxies = []

    for y in range(len(star_map)):
        for x in range(len(star_map[0])):
            if star_map[y][x] == GALAXY:
                galaxies.append((convert_coordinate(x, double_columns), convert_coordinate(y, double_rows)))

    shortest_path_length_sum = 0

    for i in range(len(galaxies) - 1):
        for j in range(i + 1, len(galaxies)):
            g_1 = galaxies[i]
            g_2 = galaxies[j]
            shortest_path_length_sum += (abs(g_1[0] - g_2[0]) + abs(g_1[1] - g_2[1]))

    print(f'Shortest Path Length Sum: {shortest_path_length_sum}\n############################\n')


def convert_coordinate(n, doubled_spaces):
    return n + (len([s for s in doubled_spaces if s < n]) * (EXPANSION_FACTOR - 1))


day_11()
