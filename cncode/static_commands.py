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

    @property
    def disabled(self):
        return 2, 3, 4, 5, 6, 9

    @property
    def as_gcode(self):
        sec = self._delay / 1000
        return f'N{self._index:03d} M501 P{self._spill} P{sec}\n' \
               f'G04 P{sec}\n'

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

    @property
    def as_gcode(self):
        return f'N{self._index:03d} M70 P{int(self._prm)} P0\n'

    @classmethod
    def from_string(cls, string: str):
        assert 'M70' in string
        inst = super().from_string(string)
        inst._type = CommandType.WELD
        inst._label = 'Weld'
        return inst


class SonoUpCommand(OneLineCommand):
    def __init__(self, index: int=0, prm: float=0.0):
        super().__init__(type_=CommandType.SONO_UP, index=index, label='Sono Up', prm=prm)

    @property
    def as_gcode(self):
        return f'N{self._index:03d} M71 P{int(self._prm)} P0\n'

    @classmethod
    def from_string(cls, string: str):
        assert 'M71' in string
        inst = super().from_string(string)
        inst._type = CommandType.SONO_UP
        inst._label = 'Sono Up'
        return inst


class SonoMidCommand(OneLineCommand):
    def __init__(self, index: int=0, prm: float=0.0):
        super().__init__(type_=CommandType.SONO_MID, index=index, label='Sono Mid', prm=prm)

    @property
    def as_gcode(self):
        return f'N{self._index:03d} M72 P{int(self._prm)} P0\n'

    @classmethod
    def from_string(cls, string: str):
        assert 'M72' in string
        inst = super().from_string(string)
        inst._type = CommandType.SONO_MID
        inst._label = 'Sono Mid'
        return inst
