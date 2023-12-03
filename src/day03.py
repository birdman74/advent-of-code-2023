import os

INPUT_DIR = 'input'
# INPUT_DIR = os.path.join('input', 'samples')

INPUT_FILE = 'day03.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)

SPACE = '.'


def day_3():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    lines = data_file.read().split('\n')

    part_number_total = 0

    symbol_coordinates = []
    number_coordinates = []

    for y in range(len(lines)):
        line = lines[y]
        num_first_char_index = -1
        num_last_char_index = -1

        for x in range(len(line)):
            char = line[x]
            if char.isnumeric():
                if num_first_char_index == -1:
                    num_first_char_index = x
                    num_last_char_index = x
                else:
                    num_last_char_index = x

                if x == len(line) - 1:
                    number_coordinates.append(((num_first_char_index, y), (num_last_char_index, y)))
            else:
                if char != SPACE:
                    symbol_coordinates.append((x, y))

                if num_last_char_index != -1:
                    number_coordinates.append(((num_first_char_index, y), (num_last_char_index, y)))
                    num_first_char_index = -1
                    num_last_char_index = -1

    for coordinates in number_coordinates:
        x_1 = coordinates[0][0]
        x_2 = coordinates[1][0]
        min_x = max(0, x_1 - 1)
        max_x = min(len(lines[0]) - 1, x_2 + 1)

        y = coordinates[0][1]
        min_y = max(0, y - 1)
        max_y = min(len(lines) - 1, y + 1)

        for symbol_location in symbol_coordinates:
            s_x = symbol_location[0]
            s_y = symbol_location[1]

            if min_x <= s_x <= max_x and min_y <= s_y <= max_y:
                part_number_total += int(lines[y][x_1:x_2 + 1])

    print(f'Part Number Total: {part_number_total}\n############################\n')


day_3()
