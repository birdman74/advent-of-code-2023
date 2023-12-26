import os
import numpy as np

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day24.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)


def day_24():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    stone_data = data_file.read().split('\n')

    positions = []
    velocities = []

    for data in stone_data:
        pieces = data.split(' @ ')
        positions.append(list(map(int, pieces[0].strip().split(', '))))
        velocities.append(list(map(int, pieces[1].strip().split(', '))))

    # Normalize the stones 1-3 with the first
    # This makes the first stone the origin (and non-moving) in a new 3d-space
    # We will have to de-normalize our answer after finding the initial rock position in the nwe 3d-space
    new_positions = []
    new_velocities = []
    pos_diff = positions[0]
    vel_diff = velocities[0]
    for i in range(4):
        new_positions.append(np.subtract(positions[i], pos_diff))
        new_velocities.append(np.subtract(velocities[i], vel_diff))

    origin = new_positions[0]

    # find the "normal" to the origin (stone #0) and the line created by stone #1
    pos1_t0 = new_positions[1]
    vel1 = new_velocities[1]
    pos1_t1 = np.add(pos1_t0, vel1)

    norm = np.cross(pos1_t0, pos1_t1)

    # Now find the intersect of our new "normal" plane with lines from stones #2 and #3
    # to give us a time reference for our rock
    pos2_t0 = new_positions[2]
    vel2 = new_velocities[2]
    pos2_in_plane, t2 = intersect(origin, norm, pos2_t0, vel2)

    pos3_t0 = new_positions[3]
    vel3 = new_velocities[3]
    pos3_in_plane, t3 = intersect(origin, norm, pos3_t0, vel3)

    t_diff = t2 - t3
    rock_vel = np.divide(np.subtract(pos2_in_plane, pos3_in_plane), t_diff)
    rock_position_in_plane = np.subtract(pos2_in_plane, np.multiply(rock_vel, t2))

    rock_position = np.ndarray.tolist(np.add(rock_position_in_plane, pos_diff))

    coordinate_sum = sum(rock_position)

    print(f'Rock initial position: {rock_position}')
    print(f'Sum of initial magical rock coordinates: {coordinate_sum}\n############################\n')


# p0: point in normal plane
# normal: normal for plane created by origin and stone 1
# pX: position of rock X
# vX: velocity of rock X
def intersect(p0, normal, pX, vX):
    # This was KEY.  Numpy was truncating my position_diff by a TON
    # which was throwing off all of these calculations.  By forcing
    # numpy to use a python object I regained my accuracy and all
    # the rest of the calculations were correct.
    position_diff = np.subtract(p0, pX, dtype=object)
    print(f'position_diff: {position_diff}')
    a = np.dot(position_diff, normal)
    print(f'a: {a}')
    b = np.dot(vX, normal)
    print(f'b: {b}')
    t = a / b
    print(f't: {t}')
    p = np.add(pX, np.multiply(vX, t))
    print(f'p: {p}\n')

    return p, t


day_24()
