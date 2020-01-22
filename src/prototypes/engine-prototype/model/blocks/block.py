class Block:
    def __init__(self, transparancy, solid):
        self._transparancy = transparancy
        self._solid = solid

        self._color = (0, 0, 0, 255)

    def get_color(self):
        return self._color



