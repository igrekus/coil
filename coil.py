import pygcode
from pygcode import Line, GCodeLinearMove, GCodeArcMoveCW, GCodeArcMoveCCW, GCodeMotion


if __name__ == '__main__':

    with open('vteslin.cnc', 'rt') as f:
        for text_line in f.readlines():
            text_line.replace(r'\\', '#')
            line = Line(text_line)
            try:
                code = line.block.gcodes[0]
                if isinstance(code, GCodeMotion):
                    print('move', line.block.gcodes)
            except LookupError:
                pass
