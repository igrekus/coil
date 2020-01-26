from pygcode import Line

from cncode.bases import MoveCommand, CommandType, ArcType


class LineToCommand(MoveCommand):
    def __init__(self, index: int=0, x: float=0.0, y: float=0.0, speed: float=0.0, spill: float=0.0,
                 prev_gui_x: float=0.0, prev_gui_y: float=0.0, prev_gcode_x: float=0.0, prev_gcode_y: float=0.0):

        super().__init__(type_=CommandType.LINE_TO, index=index, label='Line To', x=x, y=y, speed=speed, spill=spill,
                         prev_gui_x=prev_gui_x, prev_gui_y=prev_gui_y,
                         prev_gcode_x=prev_gcode_x, prev_gcode_y=prev_gcode_y)

    def __str__(self):
        return f'{self.__class__.__name__}(x={self._gui_p2.x}, y={self._gui_p2.y}, ' \
               f'speed={self._speed}, spill={self._spill})'

    @property
    def disabled(self):
        return 5, 8, 9

    @property
    def as_gcode(self):
        return 'lol'
        # sec = self._delay / 1000
        # return f'N{self._index:03d} M501 P{self._spill} P{sec}\n' \
        #        f'G04 P{sec}\n'

    @classmethod
    def from_string(cls, string: str):
        cnc_lines = [Line(l) for l in string.strip().split('\n')]
        assert len(cnc_lines) == 2

        line1, line2 = cnc_lines
        assert line1.gcodes[0].word_letter == 'N'
        assert line2.gcodes[0].word == 'G04'

        index = line1.gcodes[0].number
        spill = line1.block.modal_params[1].value
        delay = line1.block.modal_params[2].value * 1000
        return cls(index=index, spill=spill, delay=delay)
