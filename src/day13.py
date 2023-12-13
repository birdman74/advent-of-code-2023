import os

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day13.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)


def day_13():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    lines = data_file.read().split('\n')

    columns_left_of_ref_line = 0
    rows_above_ref_line = 0

    field = []
    for line in lines:
        if line:
            field.append(line)
        else:
            (cols, rows) = analyze_field(field)
            columns_left_of_ref_line += cols
            rows_above_ref_line += rows
            field = []

    (cols, rows) = analyze_field(field)
    columns_left_of_ref_line += cols
    rows_above_ref_line += rows
    field = []

    answer = columns_left_of_ref_line + (100 * rows_above_ref_line)
    print(f'Summary output: {answer}\n############################\n')


def analyze_field(field):
    height = len(field)
    width = len(field[0])

    top_matching_rows = []
    for i in range(height - 1):
        if field[i] == field[i + 1]:
            top_matching_rows.append(i)

    for row_index in top_matching_rows:
        found_reflection_point = True
        row1 = row_index
        row2 = row1 + 1
        while row1 > -1 and row2 < height:
            if field[row1] != field[row2]:
                found_reflection_point = False
                break
            row1 -= 1
            row2 += 1

        if found_reflection_point:
            return 0, row_index + 1

    matching_left_columns = []
    for i in range(width - 1):
        col1 = ''.join([line[i] for line in field])
        col2 = ''.join([line[i + 1] for line in field])

        if col1 == col2:
            matching_left_columns.append(i)

    for left_col_index in matching_left_columns:
        found_reflection_point = True
        col1_index = left_col_index
        col2_index = col1_index + 1
        while col1_index > -1 and col2_index < width:
            col1 = ''.join([line[col1_index] for line in field])
            col2 = ''.join([line[col2_index] for line in field])

            if col1 != col2:
                found_reflection_point = False
                break
            col1_index -= 1
            col2_index += 1

        if found_reflection_point:
            return left_col_index + 1, 0


day_13()
