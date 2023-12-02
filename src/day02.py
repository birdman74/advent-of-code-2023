import os

INPUT_DIR = 'input'
# INPUT_DIR = os.path.join('input', 'samples')

INPUT_FILE = 'day02.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)

RED = 'red'
GREEN = 'green'
BLUE = 'blue'

RED_MAX = 12
GREEN_MAX = 13
BLUE_MAX = 14


def day_2():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    lines = data_file.read().split('\n')

    possible_game_indices = 0
    power_sum = 0

    for line in lines:
        colon_parts = line.split(':')

        max_red = 0
        max_green = 0
        max_blue = 0

        game_index = int(colon_parts[0].split(' ')[1])
        dice_hands = colon_parts[1].split(';')
        for dice_hand in dice_hands:
            nums_and_colors = dice_hand.split(',')
            for num_and_color in nums_and_colors:
                parts = num_and_color.split(' ')
                num = int(parts[1])
                color = parts[2]
                if color == RED:
                    max_red = max(max_red, num)
                elif color == GREEN:
                    max_green = max(max_green, num)
                else:
                    max_blue = max(max_blue, num)

        if max_red <= RED_MAX and max_green <= GREEN_MAX and max_blue <= BLUE_MAX:
            possible_game_indices += game_index

        power_sum += (max_red * max_green * max_blue)

    print(f'Sum of possible game indices: {possible_game_indices}\n############################\n')
    print(f'Sum of power sets: {power_sum}\n############################\n')


day_2()
