import sys

header = """//CNC-Profile written by CN-Coil Designer
//Datetime: 11.08.2019 - 17:52:48
%
:
G71
G90
"""

footer = """
M30

"""

file = 'gcode\\rsquare.cnc'


def convert(in_file, out_file):
    with open(in_file, mode='rt', encoding='utf-8') as f:
        lines = [s.strip() for s in f.readlines()]

    cut_index = lines.index('; cut')
    retract_index = lines.index('; Retract')

    lines = lines[cut_index + 1:retract_index]

    *first, speed = lines[0].split()
    first = ' '.join(first)
    lines[0] = first

    lines = list(map(lambda s: s.replace('G1', 'G01'), lines))

    with open(f'V{out_file.upper()}.CNC', mode='wt', encoding='utf-8') as f:
        f.write(header)
        for index, line in enumerate(reversed(lines)):
            s = f'N{index + 1:03d} M500 P0\n     F12000\n     {line} Z0\n'
            print(s)
            f.write(s)
        f.write(footer)


if __name__ == '__main__':
    convert(sys.argv[1], sys.argv[2])
