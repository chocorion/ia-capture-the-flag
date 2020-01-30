from model import *

import math, sys

# Bots can't rotate more from 18°
MAX_ANGLE = 18
MAX_SPEED = 100

REAL_SPEED = 10

# http://files.magusgeek.com/csb/csb.html

DISPLAY = False

class Physic_engine:
    def __init__(self, model):
        self._model = model


    def tick(self, bots_movement):
        global DISPLAY
        for team in bots_movement.keys():
            bots = self._model.get_bots(team=team)

            for i in range(len(bots)):
                # if team == 1 and i == 1:
                #     DISPLAY = True
                # else:
                #     DISPLAY = False

                (dest_x, dest_y, speed) = bots_movement[team][i]

                speed = MAX_SPEED if speed > MAX_SPEED else speed
                speed = (speed * REAL_SPEED)/MAX_SPEED


                (x, y) = bots[i].get_coord()
                angle = bots[i].get_angle()

                new_angle = self._rotate(x, y, angle, dest_x, dest_y)

                new_x = x + math.cos(math.radians(new_angle)) * float(speed)
                new_y = y + math.sin(math.radians(new_angle)) * float(speed)

                
                bots[i].move(new_x, new_y, new_angle)


    def _distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y2)**2)


    def _get_angle(self, x, y, dest_x, dest_y):
        angle = float(math.degrees(math.atan2(dest_y - y, dest_x - x)))
        
        return angle


    def _rotate(self, x, y, angle, dest_x, dest_y):
        if x == dest_x and y == dest_y:
            new_angle = 0.
        else:
            new_angle = self._get_angle(x, y, dest_x, dest_y)

        diff = round(new_angle - angle, 2)

        if DISPLAY:
            print("({}, {}) -> ({}, {})".format(x, y, dest_x, dest_y))
            print("Angle -> {} | new angle -> {} | DIFF -> {}".format(angle, new_angle, diff))

        if diff > 180:
            diff = diff - 360

        elif diff < -180:
            diff = 360 + diff

        if diff > MAX_ANGLE:
            diff = MAX_ANGLE

        elif diff < -MAX_ANGLE:
            diff = -MAX_ANGLE

        angle += diff

        if DISPLAY:
            print("Diff -> ", diff)

        if angle > 180:
            angle = angle - 360

        elif angle < -180:
            angle = 360 + angle


        return angle