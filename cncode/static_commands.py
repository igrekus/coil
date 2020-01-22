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
        # TODO DRY this
        return f'N{self._index:03d} M70 P{int(self._prm)} P0\n'

    @classmethod
    def from_string(cls, string: str):
        # TODO check if correct class is instantiated from super().from_string() call
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


class SonoLowCommand(OneLineCommand):
    def __init__(self, index: int=0, prm: float=0.0):
        super().__init__(type_=CommandType.SONO_LOW, index=index, label='Sono Low', prm=prm)

    @property
    def as_gcode(self):
        return f'N{self._index:03d} M73 P{int(self._prm)} P0\n'

    @classmethod
    def from_string(cls, string: str):
        assert 'M73' in string
        inst = super().from_string(string)
        inst._type = CommandType.SONO_LOW
        inst._label = 'Sono Low'
        return inst


class CutWireCommand(OneLineCommand):
    def __init__(self, index: int=0, prm: float=0.0):
        super().__init__(type_=CommandType.CUT_WIRE, index=index, label='Cut wire', prm=prm)

    @property
    def as_gcode(self):
        return f'N{self._index:03d} M74 P{int(self._prm)} P0\n'

    @classmethod
    def from_string(cls, string: str):
        assert 'M74' in string
        inst = super().from_string(string)
        inst._type = CommandType.CUT_WIRE
        inst._label = 'Cut wire'
        return inst


class EmbedOnCommand(OneLineCommand):
    def __init__(self, index: int=0, prm: float=0.0):
        super().__init__(type_=CommandType.EMBED_ON, index=index, label='Embed on', prm=prm)

    @property
    def as_gcode(self):
        return f'N{self._index:03d} M75 P{int(self._prm)} P0\n'

    @classmethod
    def from_string(cls, string: str):
        assert 'M75' in string
        inst = super().from_string(string)
        inst._type = CommandType.EMBED_ON
        inst._label = 'Embed on'
        return inst


class EmbedOffCommand(OneLineCommand):
    def __init__(self, index: int=0, prm: float=0.0):
        super().__init__(type_=CommandType.EMBED_OFF, index=index, label='Embed off', prm=prm)

    @property
    def as_gcode(self):
        return f'N{self._index:03d} M76 P{int(self._prm)} P0\n'

    @classmethod
    def from_string(cls, string: str):
        assert 'M76' in string
        inst = super().from_string(string)
        inst._type = CommandType.EMBED_OFF
        inst._label = 'Embed off'
        return inst


class PullWireCommand(OneLineCommand):
    def __init__(self, index: int=0, prm: float=0.0):
        super().__init__(type_=CommandType.PULL_WIRE, index=index, label='Pull wire', prm=prm)

    @property
    def as_gcode(self):
        return f'N{self._index:03d} M77 P{int(self._prm)} P0\n'

    @classmethod
    def from_string(cls, string: str):
        assert 'M77' in string
        inst = super().from_string(string)
        inst._type = CommandType.PULL_WIRE
        inst._label = 'Pull wire'
        return inst


class HoldModuleCommand(OneLineCommand):
    def __init__(self, index: int=0, prm: float=0.0):
        super().__init__(type_=CommandType.HOLD_MODULE, index=index, label='Hold module', prm=prm)

    @property
    def as_gcode(self):
        return f'N{self._index:03d} M78 P{int(self._prm)} P0\n'

    @classmethod
    def from_string(cls, string: str):
        assert 'M78' in string
        inst = super().from_string(string)
        inst._type = CommandType.HOLD_MODULE
        inst._label = 'Hold module'
        return inst


class ReleaseModuleCommand(OneLineCommand):
    def __init__(self, index: int=0, prm: float=0.0):
        super().__init__(type_=CommandType.RELEASE_MODULE, index=index, label='Release module', prm=prm)

    @property
    def as_gcode(self):
        return f'N{self._index:03d} M79 P{int(self._prm)} P0\n'

    @classmethod
    def from_string(cls, string: str):
        assert 'M79' in string
        inst = super().from_string(string)
        inst._type = CommandType.RELEASE_MODULE
        inst._label = 'Release module'
        return inst


class BrakeOnCommand(OneLineCommand):
    def __init__(self, index: int=0, prm: float=0.0):
        super().__init__(type_=CommandType.BRAKE_ON, index=index, label='Brake on', prm=prm)

    @property
    def as_gcode(self):
        return f'N{self._index:03d} M80 P{int(self._prm)} P0\n'

    @classmethod
    def from_string(cls, string: str):
        assert 'M80' in string
        inst = super().from_string(string)
        inst._type = CommandType.BRAKE_ON
        inst._label = 'Brake on'
        return inst


class BrakeOffCommand(OneLineCommand):
    def __init__(self, index: int=0, prm: float=0.0):
        super().__init__(type_=CommandType.BRAKE_OFF, index=index, label='Brake off', prm=prm)

    @property
    def as_gcode(self):
        return f'N{self._index:03d} M81 P{int(self._prm)} P0\n'

    @classmethod
    def from_string(cls, string: str):
        assert 'M81' in string
        inst = super().from_string(string)
        inst._type = CommandType.BRAKE_OFF
        inst._label = 'Brake off'
        return inst


class ThermodeMidCommand(OneLineCommand):
    def __init__(self, index: int=0, prm: float=0.0):
        super().__init__(type_=CommandType.THERM_MID, index=index, label='Thermode Mid', prm=prm)

    @property
    def as_gcode(self):
        return f'N{self._index:03d} M82 P{int(self._prm)} P0\n'

    @classmethod
    def from_string(cls, string: str):
        assert 'M82' in string
        inst = super().from_string(string)
        inst._type = CommandType.THERM_MID
        inst._label = 'Thermode Mid'
        return inst


class ThermodeUpCommand(OneLineCommand):
    def __init__(self, index: int=0, prm: float=0.0):
        super().__init__(type_=CommandType.THERM_UP, index=index, label='Thermode Up', prm=prm)

    @property
    def as_gcode(self):
        return f'N{self._index:03d} M83 P{int(self._prm)} P0\n'

    @classmethod
    def from_string(cls, string: str):
        assert 'M83' in string
        inst = super().from_string(string)
        inst._type = CommandType.THERM_UP
        inst._label = 'Thermode Up'
        return inst
