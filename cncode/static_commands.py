from cncode.bases import Command, CommandType


class FillCommand(Command):
    def __init__(self, text, previous=None):
        super().__init__(text, previous)
        self._label = 'Fill'
        self._type = CommandType.FILL

        self._parse()

    def __str__(self):
        return f'FillCnCommand(n={self._index} p1={self._spill} p2={self._delay})'

    def __getitem__(self, item):
        if item in range(2, 7):
            return ''
        elif item == 0:
            return self._index
        elif item == 1:
            return self._label
        elif item == 7:
            return self._spill
        elif item == 8:
            return self._delay
        elif item == 9:
            return ''

    def _parse(self):
        super()._parse()
        assert len(self._cnc_lines) == 2

        line1, line2 = self._cnc_lines
        assert line1.gcodes[0].word_letter == 'N'
        assert line2.gcodes[0].word == 'G04'

        self._index = line1.gcodes[0].number
        self._spill = line1.block.modal_params[1].value
        self._delay = line1.block.modal_params[2].value * 1000

    @property
    def enabled(self):
        return 1, 7, 8
