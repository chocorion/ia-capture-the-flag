from model.map import *
from model.blocks import *
from model.game_objects import *
from model.physic_engine import Physic_engine
from view import *

from ai import *

from ruleset import ruleset

from random import (randrange, uniform)
from ai.astar import *



class Game_model:

    def __init__(self, map_filename):
        # Model need an inner representation of the game
        self._cell_size = 100
        self._default_bot_radius = 40

        # While initializing players
        self._current_team_registration = 0

        self._teams = dict()

        self._map = Map(filename=map_filename, cell_size=self._cell_size)
        self._physic_engine = Physic_engine(self)
        self._generate_bots(bots_per_squad=ruleset["TEAM_SIZE"])

        self._astar_start_cell = None
        self._astar_end_cell = None

        self._ai_destination = None


    def _generate_bots(self, bots_per_squad):
        self._bots = [[], []]
        spawn_zones = self._map.get_spawn_zones()

        [x1, y1, w1, h1] = spawn_zones[1]
        [x2, y2, w2, h2] = spawn_zones[2]      

        infos = (
            [1] + spawn_zones[1],
            [2] + spawn_zones[2]
        )

        margin = self._default_bot_radius/self._cell_size

        for i in range(bots_per_squad):
            for (team, x, y, w, h) in infos:
                self._bots[team - 1].append(
                    Bot(
                        team=team,
                        x = round(uniform(x + margin, x + w - margin), 2) * self._cell_size,
                        y = round(uniform(y + margin, y + h - margin), 2) * self._cell_size,
                        radius=self._default_bot_radius
                    )
                )
    
    def tick(self, dt):
        result = {
            1: None,
            2: None
        }

        for team in self._teams.keys():
            datas = []

            for bot in self._bots[team - 1]:
                (x, y) = bot.get_coord()
                angle = bot.get_angle

                datas.append((x, y, angle, self._ai_destination))

            result[team] = self._teams[team].tick(datas)

        self._physic_engine.tick(result, dt)


    def set_ai(self, player):
        self._current_team_registration += 1

        self._teams[self._current_team_registration] = player(self._current_team_registration, ruleset["TEAM_SIZE"], self.get_map())


    def get_map(self):
        return self._map

    
    def get_bots(self, team=-1):
        if team == -1:
            return self._bots[0] + self._bots[1]

        # Must verify index
        return self._bots[team - 1]

    def get_cell_size(self):
        return self._cell_size

    def build_graph(self):
        nodeGraph = []
        for x in range(self._map.get_width()):
            for y in range(self._map.get_height()):
                insertNode(x, y, str(self._map.get_tile(x,y)), nodeGraph)
        return nodeGraph

    def mark_path(self):
        nodeGraph = self.build_graph()

        # Get start and goal node
        start = list(filter(lambda n: n.x == self._astar_start_cell[0] and n.y ==  self._astar_start_cell[1] , nodeGraph))[0]
        goal  = list(filter(lambda n: n.x == self._astar_end_cell[0]   and n.y ==  self._astar_end_cell[1], nodeGraph))[0]
        
        res_a_star = a_star(start, goal, nodeGraph)
        
        for node in res_a_star[0]:
            self._map.mark(node.x, node.y)

    
    def mark_start_cell(self, x, y):
        cell_x = x // self._cell_size
        cell_y = y // self._cell_size

        if not self._map.is_empty(cell_x, cell_y):
            return

        if self._astar_start_cell != None:
            self._map.unmark(self._astar_start_cell[0], self._astar_start_cell[1])
            
        self._astar_start_cell = (cell_x, cell_y)
        self._map.mark_start_cell(cell_x, cell_y)
        
        self.set_ai_destination(x, y)
        
        if self._astar_end_cell != None:
            self._map.clear_path()
            self.mark_path()


    def mark_end_cell(self, x, y):
        cell_x = x // self._cell_size
        cell_y = y // self._cell_size

        if not self._map.is_empty(cell_x, cell_y):
            return

        if self._astar_end_cell != None:
            self._map.unmark(self._astar_end_cell[0], self._astar_end_cell[1])
        
        self._astar_end_cell = (cell_x, cell_y)
        self._map.mark_end_cell(cell_x, cell_y)

        self.set_ai_destination(x, y)

        if self._astar_start_cell != None:
            self._map.clear_path()
            self.mark_path()


    def set_ai_destination(self, x, y):
        x = int(x//self._cell_size)
        y = int(y//self._cell_size)

        if not self._map.is_solid(x, y):
            self._ai_destination = (x, y)
            print("Ai destination set to {}:{}".format(x, y))
        
        else:
            print("Ai destination can't be set in a solid block !")
