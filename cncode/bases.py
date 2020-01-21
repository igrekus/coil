from abc import ABC, abstractmethod

from pygcode import Line
from cncode import CommandType


class Command(ABC):
    def __init__(self, text):
        self._text: str = text
        self._lines: list = text.split('\n')
        self._cnc_lines: list = list()

        self._type: CommandType = CommandType.UNDEFINED

        self._index: int = 0
        self._label: str = 'undefined'
        self._spill: float = 0.0   # first P parameter
        self._delay: float = 0.0   # second P parameter
        self._prm: float = 0.0   # arbitrary parameter

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

    @abstractmethod
    def _parse(self):
        self._cnc_lines = [Line(l) for l in self._lines]

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
