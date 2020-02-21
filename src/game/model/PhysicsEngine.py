from service.Physics import Physics
from service.Config import Config
from domain.Map import Map

class PhysicsEngine(Physics):
    """
    Methods used to apply physics to the game world

    Attributes:
        ruleset (Ruleset) : The set of rules needed to make objects behave
        map (Map) : The game world
        deltaTime (int) : Time in milliseconds since last tick
    """

    def __init__(self, ruleset, map_):
        self._ruleset = ruleset
        self._map = map_

        self.collisions_maps = dict()
        self.collisions_maps_dividers = dict()


    def tick(self, deltaTime):
        """
        Update deltaTime
        """
        self.deltaTime = deltaTime

    def checkSpeed(self, bot, target_speed):
        """
        Checks whether a target speed is correct for a bot.

        Returns:
            target_speed (int) : A correct target speed for this bot.
        """
        max_speed = float(self._ruleset["SpeedMultiplier"]) * bot.max_speed

        if target_speed > max_speed:
            target_speed = max_speed
        if target_speed < 0:
            target_speed = 0

        return target_speed

    def checkAngle(self, bot, target_x, target_y):
        """
        Checks whether a target point is correct for a bot.

        Returns:
            target_angle (int) : A correct target angle for this bot.
        """
        new_angle = Physics.getAngle( bot.x, bot.y, target_x, target_y)

        delta_angle = new_angle - bot.angle

        if delta_angle > 180:
            delta_angle = delta_angle - 360

        elif delta_angle < -180:
            delta_angle = 360 + delta_angle
        
        max_angle = float(self._ruleset["RotationMultiplier"]) * bot.max_rotate
        max_angle = max_angle * self.getDeltaTimeModifier()

        if abs(delta_angle) > max_angle :
            delta_angle = max_angle if delta_angle > 0 else -max_angle
            
        return bot.angle + delta_angle

    def getDeltaTimeModifier(self):
        """
        This is the multiplier for all physics operations, since deltaTime can be inconsistent.
        """
        return (self.deltaTime / (1000 / (30 * Config.TimeRate())))

    def checkCollision(self, collision_map, x, y, target_x, target_y, cap_x, cap_y):
        """
        Checks whether a target's path collides with the map.

        Returns:
            position (int,int) : The first valid position.
        """
        
        dx = abs(target_x - x)
        dy = abs(target_y - y)

        current_x = x
        current_y = y

        last_x = x
        last_y = y

        n = int(1 + dx + dy)

        x_inc = 1 if (target_x > x) else -1
        y_inc = 1 if (target_y > y) else -1

        error = dx - dy

        dx *= 2
        dy *= 2
        
        for i in range(n, 0, -1):

            if cap_x != None and cap_y != None and cap_x == last_x and cap_y == last_y:
                return (last_x,last_y)
            
            if self.collisions_maps[collision_map][int(current_x // self.collisions_maps_dividers[collision_map])][int(current_y // self.collisions_maps_dividers[collision_map])]:
                return (last_x, last_y)

            last_x = current_x
            last_y = current_y

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
                
        return (target_x, target_y)

    def createCollisionMap(self, name, padding):

        divider = 10 # 1 / round(Map.BLOCKSIZE / padding)
        self.collisions_maps_dividers[name] = divider

        collisions_map_padding = int(padding // (Map.BLOCKSIZE // divider))
        collisions_map_width = int(self._map.blockWidth * divider)
        collisions_map_height = int(self._map.blockHeight * divider)

        self.collisions_maps[name] = [[False for i in range(0,collisions_map_height)] for j in range(0,collisions_map_width)]

        block_size_factored = int(Map.BLOCKSIZE // divider)

        (x,y) = (0,0)
        for blockline in self._map.blocks:
            for block in blockline:
                if block.solid:
                    for rx in range(- collisions_map_padding, block_size_factored + collisions_map_padding):
                        for ry in range(- collisions_map_padding, block_size_factored + collisions_map_padding):
                            nx = int(x + rx)
                            ny = int(y + ry)
                            
                            if nx >= 0 and ny >= 0 and nx < collisions_map_width and ny < collisions_map_height:
                                # print("{} {}".format(nx,ny))
                                self.collisions_maps[name][nx][ny] = True

                y += block_size_factored
            y = 0
            x += block_size_factored