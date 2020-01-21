from pygcode import Line

from cncode.bases import Command, CommandType, OneLineCommand


class FillCommand(Command):
    def __init__(self, index: int=0, spill: float=0.0, delay: float=0.0):
        super().__init__(type_=CommandType.FILL,
                         index=index,
                         label='Fill',
                         spill=spill,
                         delay=delay,
                         prm=0.0)

    def __str__(self):
        return f'FillCnCommand(n={self._index} spill={self._spill} delay={self._delay})'

    @property
    def disabled(self):
        return 2, 3, 4, 5, 6, 9

    @property
    def as_gcode(self):
        sec = self._delay / 1000
        return f'N{self._index:03d} M501 P{self._spill} P{sec}\n' \
               f'G04 P{sec}'

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


class WeldCommand(OneLineCommand):
    def __init__(self, index: int=0, prm: float=0.0):
        super().__init__(type_=CommandType.WELD, index=index, label='Weld', prm=prm)

    def __str__(self):
        return f'FillCnCommand(n={self._index} prm={self._prm})'

    @property
    def as_gcode(self):
        return f'N{self._index:03d} M70 P{int(self._prm)} P0'

    @classmethod
    def from_string(cls, string: str):
        inst = super().from_string(string)
        inst._type = CommandType.WELD
        inst._label = 'Weld'
        return inst
