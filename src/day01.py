import os

INPUT_DIR = 'input'
INPUT_FILE = 'day01.txt'

# INPUT_DIR = os.path.join('input', 'samples')
# INPUT_FILE = "day01-1.txt"
# INPUT_FILE = "day01-2.txt"


NUM_SUBS = {('one', '1'),
            ('two', '2'),
            ('three', '3'),
            ('four', '4'),
            ('five', '5'),
            ('six', '6'),
            ('seven', '7'),
            ('eight', '8'),
            ('nine', '9')}

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)


def day_1():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f"Input file: {input_file}")

    data_file = open(input_file)
    lines = data_file.read().split("\n")

    output = 0

    for line in lines:
        first_int_char_index = -1
        first_int_char = ''
        last_int_char_index = -1
        last_int_char = ''

        for i in range(len(line)):
            if line[i].isnumeric():
                last_int_char_index = i
                last_int_char = line[i]
                if first_int_char == '':
                    first_int_char_index = i
                    first_int_char = line[i]

        if first_int_char_index == -1:
            first_int_char_index = len(line)

        for (num_name, num_char) in NUM_SUBS:
            i = line.find(num_name)
            if -1 < i < first_int_char_index:
                first_int_char_index = i
                first_int_char = num_char

            i = line.rfind(num_name)
            if last_int_char_index < i:
                last_int_char_index = i
                last_int_char = num_char

        output += int(first_int_char + last_int_char)

    print(f"Sum of calibration values: {output}\n############################\n")


day_1()
