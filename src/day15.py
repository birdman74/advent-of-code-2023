import os

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day15.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)

DASH = '-'
EQUALS = '='


def day_15():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    lines = data_file.read().split('\n')

    total_focusing_power = 0

    steps = lines[0].split(',')

    # key = box num, val = {key = label, value = lens array index}
    boxes = {}

    for step in steps:
        if step.find(EQUALS) > 0:
            parts = step.split(EQUALS)
            label = parts[0]
            f_l = int(parts[1])
            box_num = hash15(label)
            if box_num in boxes.keys():
                box = boxes[box_num]
                box[label] = f_l
            else:
                boxes[box_num] = {label: f_l}
        else:
            label = step[0:len(step) - 1]
            box_num = hash15(label)
            if box_num in boxes.keys():
                try:
                    lenses = boxes[box_num]

                    del lenses[label]
                except KeyError:
                    pass

    for i in range(256):
        try:
            box = boxes[i]
            focusing_power = 0
            box_num = i + 1
            for lens_index, label in enumerate(box):
                focusing_power += (box_num * (lens_index + 1) * box[label])

            total_focusing_power += focusing_power
        except KeyError:
            pass

    print(f'Total focusing power: {total_focusing_power}\n############################\n')


def hash15(label):
    i = 0
    for c in label:
        i += ord(c)
        i *= 17
        i %= 256

    return i


day_15()
