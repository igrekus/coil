class CNCommand:

    def __init__(self):
        self._index: int = 0


class CNFile:
    def __init__(self, text):
        self._text = text

        print('>>>>', text)
