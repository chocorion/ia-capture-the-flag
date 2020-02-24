from model import *

import math, sys

# Bots can't rotate more from 18°
maxAngle = 18
maxSpeed = 100

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

                speed = maxSpeed if speed > maxSpeed else speed
                speed = (speed * REAL_SPEED)/maxSpeed


                (x, y) = bots[i].get_coord()
                angle = bots[i].get_angle()

                newAngle = self._rotate(x, y, angle, dest_x, dest_y)

                dx = math.cos(math.radians(newAngle))
                dy = math.sin(math.radians(newAngle))

                newX = x + dx * float(speed) * dt/1000
                newY = y + dy * float(speed) * dt/1000

                botRadius = bots[i].get_radius()
                
                # Check collision with the border of the circle
                collision = self._check_collisionMap(
                    x + dx * botRadius,
                    y + dy * botRadius,
                    newX + dx * botRadius,
                    newY + dy * botRadius
                )
                
                newX = newX if collision[0] == -1 else collision[0] - dx * botRadius
                newY = newY if collision[1] == -1 else collision[1] - dy * botRadius

                bots[i].move(newX, newY, newAngle)


    def _check_collisionMap(self, x, y, dest_x, dest_y):
        cell_size = self._model.get_cellSize()

        dx = abs(dest_x - x)
        dy = abs(dest_y - y)

        currentX = x
        currentY = y

        n = int(1 + dx + dy)

        xInc = 1 if (dest_x > x) else -1
        yInc = 1 if (dest_y > y) else -1

        error = dx - dy

        dx *= 2
        dy *= 2
        
        for i in range(n,0,-1):
            
            if self._model.get_map().is_solid(int(currentX // cell_size), int(currentY // cell_size)):
                return (currentX, currentY)

            if error > 0:
                currentX += xInc
                error -= dy
            elif error < 0:
                currentY += yInc
                error += dx
            elif error == 0:
                currentX += xInc
                currentY += yInc
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
            newAngle = 0.
        else:
            newAngle = self._get_angle(x, y, dest_x, dest_y)

        diff = round(newAngle - angle, 2)

        if DISPLAY:
            print("({}, {}) -> ({}, {})".format(x, y, dest_x, dest_y))
            print("Angle -> {} | new angle -> {} | DIFF -> {}".format(angle, newAngle, diff))

        if diff > 180:
            diff = diff - 360

        elif diff < -180:
            diff = 360 + diff

        if diff > maxAngle:
            diff = maxAngle

        elif diff < -maxAngle:
            diff = -maxAngle

        angle += diff

        if DISPLAY:
            print("Diff -> ", diff)

        if angle > 180:
            angle = angle - 360

        elif angle < -180:
            angle = 360 + angle


        return angle