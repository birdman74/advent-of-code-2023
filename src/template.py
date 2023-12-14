import os

INPUT_DIR = os.path.join('input', 'samples')
# INPUT_DIR = 'input'

INPUT_FILE = 'dayDAYNUM.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)


def day_DAYNUM():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    lines = data_file.read().split('\n')

    output = 0

    print(f': {output}\n############################\n')


day_DAYNUM()
