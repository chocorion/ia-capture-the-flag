from model import *

import math

# Bots can't rotate more from 18°
MAX_ANGLE = 18
MAX_SPEED = 20

# http://files.magusgeek.com/csb/csb.html

class Physic_engine:
    def __init__(self, model):
        self._model = model


    def tick(self, bots_movement):
        for team in bots_movement.keys():
            bots = self._model.get_bots(team=team)

            for i in range(len(bots)):
                (dest_x, dest_y, speed) = bots_movement[team][i]

                speed = MAX_SPEED if speed > MAX_SPEED else speed

                (x, y) = bots[i].get_coord()
                angle = bots[i].get_angle()

                new_angle = self._rotate(x, y, angle, dest_x, dest_y)

                new_x = x + math.cos(new_angle) * speed
                new_y = y + math.sin(new_angle) * speed

                bots[i].move(new_x, new_y, new_angle)


    def _distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y2)**2)


    def _get_angle(self, x, y, dest_x, dest_y):
        distance = self._distance(x, y, dest_x, dest_y)
        

        dx = (dest_x - x)/distance
        dy = (dest_y - y)/distance

        angle = math.acos(dx) * 180. / math.pi

        # if dy < 0:
        #     a = 360. - a

        return angle


    def _rotate(self, x, y, angle, dest_x, dest_y):
        if x == dest_x and y == dest_y:
            new_angle = 0.
        else:
            new_angle = self._get_angle(x, y, dest_x, dest_y)

        if new_angle > MAX_ANGLE:
            new_angle = MAX_ANGLE

        elif new_angle < -MAX_ANGLE:
            new_angle = -MAX_ANGLE

        angle += new_angle
        angle %= 360.

        return angle