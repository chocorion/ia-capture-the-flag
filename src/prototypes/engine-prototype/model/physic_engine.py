from model import *

import math, sys

# Bots can't rotate more from 18°
MAX_ANGLE = 18
MAX_SPEED = 100

REAL_SPEED = 600

# http://files.magusgeek.com/csb/csb.html

DISPLAY = False

class Physic_engine:
    def __init__(self, model):
        self._model = model


    def tick(self, bots_movement, dt):
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

                new_x = x + math.cos(math.radians(new_angle)) * float(speed) * dt/1000
                new_y = y + math.sin(math.radians(new_angle)) * float(speed) * dt/1000

                collision = self._check_collision_map(x,y,new_x,new_y)
                
                new_x = new_x if collision[0] == -1 else collision[0]
                new_y = new_y if collision[1] == -1 else collision[1]

                bots[i].move(new_x, new_y, new_angle)


    def _check_collision_map(self, x, y, dest_x, dest_y):
        cell_size = self._model.get_cell_size()

        dx = abs(dest_x - x)
        dy = abs(dest_y - y)

        current_x = x
        current_y = y

        n = int(1 + dx + dy)

        x_inc = 1 if (dest_x > x) else -1
        y_inc = 1 if (dest_y > y) else -1

        error = dx - dy

        dx *= 2
        dy *= 2
        
        for i in range(n,0,-1):
            
            if self._model.get_map().is_solid(int(current_x // cell_size), int(current_y // cell_size)):
                return (current_x, current_y)

            if error > 0:
                current_x += x_inc
                error -= dy
            elif error < 0:
                current_y += y_inc
                error += dx
            elif error == 0:
                current_x += x_inc
                current_y += y_inc
                error -= dy
                error += dx
                n -= 1
                
        return (-1,-1)
        



        

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