import os
import datetime


class JSCutFile:
    header = f"""//CNC-Profile written by Coil\n//Datetime: {datetime.datetime.now().strftime('%d.%m.%Y - %H:%M:%S')}\n%\n:\nG71\nG90\n\n"""

    footer = """\nM30\n"""

    file = 'gcode\\rsquare.cnc'

    def __init__(self, in_filename):
        self._in_filename = in_filename
        self._out_file = ''

        self._raw_lines = list()
        self._converted = list()

        self._load()
        self._parse()

    def _load(self):
        lines = None
        if os.path.isfile(self._in_filename):
            with open(self._in_filename, mode='rt') as f:
                lines = [s.strip() for s in f.readlines()]

        if not lines:
            return
        try:
            cut_index = lines.index('; cut')
            retract_index = lines.index('; Retract')
        except ValueError:
            print('ERROR: wrong input file format')
            return

        lines = lines[cut_index + 1:retract_index]

        *first, speed = lines[0].split()
        first = ' '.join(first)
        lines[0] = first

        self._raw_lines = reversed(list(map(lambda s: s.replace('G1', 'G01'), lines)))

    def _parse(self):
        self._converted = [
            f'N{index + 1:03d} M500 P0\n     F12000\n     {line} Z0\n'
            for index, line
            in enumerate(self._raw_lines)
        ]

    def save(self, name='OUT'):
        fn = f'V{name}.CNC'
        with open(fn, mode='wt', encoding='utf-8') as f:
            f.write(self.text)
        self._out_file = fn

    @property
    def text(self):
        return self.header + ''.join(self._converted) + self.footer

    @property
    def out_filename(self):
        return self._out_file
