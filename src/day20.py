import os
from enum import Enum
from functools import reduce

# INPUT_DIR = os.path.join('input', 'samples')
INPUT_DIR = 'input'

INPUT_FILE = 'day20.txt'

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(MODULE_DIR, '..')
INPUT_SOURCE_DIR = os.path.join(PROJECT_DIR, INPUT_DIR)

BROADCASTER_NAME = 'broadcaster'
HI = 'hi'
LO = 'lo'


class ModuleType(Enum):
    FLIP_FLOP = '%'
    CONJUNCTION = '&'
    BROADCASTER = 'b'


def day_20():
    do_stuff()


def do_stuff():
    input_file = os.path.join(INPUT_SOURCE_DIR, INPUT_FILE)
    print(f'Input file: {input_file}')

    data_file = open(input_file)
    module_map = data_file.read().split('\n')
    modules = {}

    def add_to_modules(mod_name):
        if mod_name not in modules.keys():
            modules[mod_name] = Module(mod_name)

        return modules[mod_name]

    for module_setup in module_map:
        pieces = module_setup.split(' -> ')
        m_type = ModuleType(pieces[0][0])
        name = pieces[0][1:] if m_type != ModuleType.BROADCASTER else pieces[0]
        outputs = pieces[1].split(', ')

        mod = add_to_modules(name)
        mod.module_type = m_type
        for output_name in outputs:
            o_module = add_to_modules(output_name)
            mod.output_modules.append(o_module)
            o_module.input_modules.append(mod)

    rx_sent_lo = False
    button_presses = 0
    while not rx_sent_lo:
        button_presses += 1
        # print(f'Executing button press #{button_presses}')
        rx_sent_lo = push_button(modules, button_presses)

    button_presses = reduce(lambda x, y: x*y, [m for m in modules['qn'].first_input_hi.values()])

    print(f'Number of button presses to get "rx" sent a low pulse: {button_presses}\n############################\n')


def push_button(modules, push_count):
    lo_pulses = 1 # button push
    hi_pulses = 0

    active_modules = [['button', BROADCASTER_NAME, LO]]
    while len(active_modules) > 0:
        new_active_modules = []
        for from_name, mod_name, pulse in active_modules:
            if mod_name == 'rx':
                # print(f'{from_name} -> {pulse} -> {mod_name}')
                if pulse == LO:
                    return True
                elif len([v for v in modules[from_name].past_input_values.values() if v == HI]) > 0:
                    for input_name in modules[from_name].past_input_values.keys():
                        if (modules[from_name].past_input_values[input_name] == HI and
                                input_name not in modules[from_name].first_input_hi.keys()):
                            modules[from_name].first_input_hi[input_name] = push_count
                        if len(modules[from_name].first_input_hi) == len(modules[from_name].past_input_values):
                            return True
                    # modules[mod_name].print_upstream_state(1, 0)
                    # print('')

            new_lo_pulses, new_hi_pulses = modules[mod_name].process(pulse, from_name, new_active_modules)
            lo_pulses += new_lo_pulses
            hi_pulses += new_hi_pulses

        active_modules = new_active_modules

    return False


class Module:
    def __init__(self, name):
        self.name = name
        self.module_type = None
        self.input_modules = []
        self.output_modules = []
        self.on = False
        self.past_input_values = {}
        self.first_input_hi = {}

    def __repr__(self):
        return f'{self.name}: {self.module_type.value}, on={self.on}'

    def orig_name(self):
        return f'{self.module_type.value}{self.name}'

    def debug_state(self):
        return (f'{self.orig_name()}, on={self.on}, '
                f'inputs={[m.orig_name() + '-' + self.past_input_values[m.name] for m in self.input_modules]}')

    def print_upstream_state(self, this_level, more_levels):
        indent = '\t' * this_level
        for i_mod in self.input_modules:
            print(indent + i_mod.debug_state())
            if more_levels > 0:
                i_mod.print_upstream_state(this_level + 1, more_levels - 1)

    def process(self, pulse, from_name, new_active_modules):
        lo_pulse_count = 0
        hi_pulse_count = 0

        match self.module_type:
            case ModuleType.FLIP_FLOP:
                if pulse == LO:
                    self.on = not self.on
                    new_pulse = HI if self.on else LO
                    if new_pulse == LO:
                        lo_pulse_count += len(self.output_modules)
                    else:
                        hi_pulse_count += len(self.output_modules)
                    for o in self.output_modules:
                        new_active_modules.append([self.name, o.name, new_pulse])
            case ModuleType.CONJUNCTION:
                if len(self.past_input_values) == 0:
                    for mod in self.input_modules:
                        self.past_input_values[mod.name] = LO

                self.past_input_values[from_name] = pulse
                past_vals = set(self.past_input_values.values())
                new_pulse = LO if len(past_vals) == 1 and list(past_vals)[0] == HI else HI
                if new_pulse == LO:
                    lo_pulse_count += len(self.output_modules)
                else:
                    hi_pulse_count += len(self.output_modules)
                for o in self.output_modules:
                    new_active_modules.append([self.name, o.name, new_pulse])
            case ModuleType.BROADCASTER:
                lo_pulse_count = len(self.output_modules)
                for o in self.output_modules:
                    new_active_modules.append([self.name, o.name, pulse])

        return lo_pulse_count, hi_pulse_count


day_20()

# % flip-flop  : init: off; high=no change; lo toggle on/off; if off -> on, send hi; if on -> off send lo

# & conjunction: remember hi/lo from each input, init: lo
#                store pulse mem, then if all inputs high: send lo, else send hi

# broadcaster  : send same pulse to all outputs that it receives

# button       : when pushed sends lo to broadcaster

# &qn -> rx
# qn inputs must be hi: &qz &cq &jx &tt

# qz: &zq must be low
# cq: &kx must be low
