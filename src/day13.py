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
    field_number = 1
    for line in lines:
        if line:
            field.append(line)
        else:
            print(f'Analyzing Field {field_number}')
            (cols, rows) = analyze_field(field)
            print(f'Results: ({cols}, {rows})')
            columns_left_of_ref_line += cols
            rows_above_ref_line += rows
            field = []
            field_number += 1

    print(f'Analyzing Field {field_number}')
    (cols, rows) = analyze_field(field)
    print(f'Results: ({cols}, {rows})')
    columns_left_of_ref_line += cols
    rows_above_ref_line += rows

    answer = columns_left_of_ref_line + (100 * rows_above_ref_line)
    print(f'Summary output: {answer}\n############################\n')


def analyze_field(field):
    row_results = work_the_list(field)

    if row_results == 0:
        width = len(field[0])
        columns = []
        for i in range(width):
            columns.append(column(field, i))
        return work_the_list(columns), 0

    return 0, row_results


def work_the_list(lines):
    line_count = len(lines)
    matches = []

    if possible_smudge(lines[0], lines[1]):
        return 1
    elif possible_smudge(lines[line_count - 2], lines[line_count - 1]):
        return line_count - 1
    else:
        for i in range(line_count - 1):
            for j in range(i + 1, line_count):
                if lines[i] == lines[j]:
                    matches.append((i, j))

        for match in matches:
            if (match[1] - match[0]) % 2 == 0:
                continue

            start_low_index = int(match[1] - ((match[1] - match[0] + 1) / 2))
            low_index = start_low_index
            high_index = low_index + 1
            smudge_pair = ()

            while low_index > -1 and high_index < line_count:
                pair = (low_index, high_index)
                low_index -= 1
                high_index += 1

                if pair not in matches:
                    if smudge_pair:
                        smudge_pair = ()
                        break

                    smudge_pair = pair

            if smudge_pair and possible_smudge(lines[smudge_pair[0]], lines[smudge_pair[1]]):
                return start_low_index + 1

    return 0


def column(field, index):
    return ''.join([line[index] for line in field])


def possible_smudge(line1, line2):
    diffs = 0
    for i in range(len(line1)):
        if line1[i] != line2[i]:
            diffs += 1
        if diffs > 1:
            return False

    return diffs == 1


day_13()
