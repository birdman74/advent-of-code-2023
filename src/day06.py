import os

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day06.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)


def day_06():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    lines = data_file.read().split('\n')

    race_time = int(lines[0].split(':')[1].replace(' ', ''))
    record = int(lines[1].split(':')[1].replace(' ', ''))

    button_time = 0
    moving_time = 0
    winning_combos = 0

    if race_time % 2 == 0:
        button_time = race_time / 2
        moving_time = race_time / 2
        winning_combos -= 1
    else:
        button_time = (race_time + 1) / 2
        moving_time = button_time - 1

    while button_time * moving_time > record:
        winning_combos += 2

        button_time += 1
        moving_time -= 1

    print(f'Winning Combos: {winning_combos}\n############################\n')


day_06()
