from model.game_objects.game_objet import Game_object

RED = (255, 0, 0, 255)
BLUE = (0, 0, 255, 255)

class Bot(Game_object):
    def __init__(self, team, x=0., y=0.):
        super().__init__(x, y)

        self._team = team
        self._angle = 0
        self._speed = 0.
        self._color = BLUE if team == 2 else RED


    def teleport(self, x, y):
        self._x = x
        self._y = y

    def get_team_color(self):
        return self._color