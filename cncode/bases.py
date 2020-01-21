from abc import ABC, abstractmethod

from cncode import CommandType


class Command(ABC):
    def __init__(self, type_: CommandType = CommandType.UNDEFINED, index: int=0, label: str='undefined', spill: float=0.0, delay: float=0.0, prm: float=0.0):
        self._type: type_
        self._index: int = index
        self._label: str = label
        self._spill: float = spill   # first P parameter
        self._delay: float = delay   # second P parameter
        self._prm: float = prm       # arbitrary parameter

    def __str__(self):
        return f'AbstractCommand()'

    def __getitem__(self, item):
        if item == 0:
            return self._index
        elif item == 1:
            return self._label
        elif item == 2:
            return ''
        elif item == 3:
            return ''
        elif item == 4:
            return ''
        elif item == 5:
            return ''
        elif item == 6:
            return ''
        elif item == 7:
            return self._spill
        elif item == 8:
            return self._delay
        elif item == 9:
            return self._prm

    @property
    @abstractmethod
    def disabled(self):
        pass

    @property
    def length(self):
        return 0

    @property
    def is_move(self):
        return False

    @property
    @abstractmethod
    def as_gcode(self):
        pass

    @classmethod
    @abstractmethod
    def from_string(cls, string: str):
        pass
