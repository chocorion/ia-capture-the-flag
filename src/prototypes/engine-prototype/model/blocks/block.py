class Block:
    def __init__(self, transparancy, solid, color=(0, 0, 0, 255), name='default'):
        self._transparancy = transparancy
        self._solid = solid

        self._name = name
        self._color = color

    def get_color(self):
        return self._color

    def get_name(self):
        return self._name


