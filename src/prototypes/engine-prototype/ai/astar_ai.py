from ai.ai_interface import AI
from ai.bot import Bot
from ai.astar import *
from random import randrange
import math

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

class Astar_AI(AI):
    def __init__(self, team, number_of_bots, game_map):
        super().__init__(team, number_of_bots, game_map)
        #Only one path for all bots actually
        self._res_a_star = []
        self._bots = [Bot() for i in range(number_of_bots)]

        for bot_index in range(len(self._bots)):
            self._bot_set_random_dest(bot_index)
            self._bots[bot_index].save_pos()

    def build_graph(self, map_width, map_height):
        nodeGraph = []
        for x in range(map_width):
            for y in range(map_height):
                insertNode(x, y, 
                str(super().get_map().get_tile(x,y)),
                nodeGraph)
        return nodeGraph

    #Just for initialize a random position
    def _bot_set_random_dest(self, bot_index):
        map_cell_size = super().get_map().get_cell_size()
        map_width     = super().get_map().get_width()
        map_height    = super().get_map().get_height()

        self._bots[bot_index].set_dest(
            randrange(map_cell_size, map_width * map_cell_size),
            randrange(map_cell_size, map_height * map_cell_size)
        )
    
    def _bot_set_astar_dest(self,bot_index,x,y):
        map_cell_size = super().get_map().get_cell_size()
        map_width     = super().get_map().get_width()
        map_height    = super().get_map().get_height()

        #If the path is empty (not calculated)
        if len(self._res_a_star) == 0:
            #Build the graph, then find our start position(should be tell by the motor)
            #Find a random goal
            nodeGraph = self.build_graph(map_width, map_height)
            start = self.find_start(nodeGraph,bot_index)
            goal  = self.find_goal(map_height, map_width, map_cell_size, nodeGraph)

            #If a_star is not null (no path)
            res = a_star(start, goal, nodeGraph)
            if res :
                self._res_a_star = res 
            
            #Clear the memory not sure if necessary
            del nodeGraph
            del res
        
        #Once we have a path
        else:
            # self._res_a_star[0] is the path, since we pop after each call to this function,
            # we must check if not empty
            if self._res_a_star[0]:
                #Pick the first node of current path (olders are deleted)
                node = self._res_a_star[0][0]
                (dest_x, dest_y) = node.x, node.y
                #Send the destination with the good coordinates
                self._bots[bot_index].set_dest(dest_x * map_cell_size,dest_y * map_cell_size)
                to_delete =self._res_a_star[0].pop(0)
                del to_delete
            #Finally if the path is empty, reset the astar 
            else:
                del self._res_a_star
                self._res_a_star = []

    def find_goal(self,map_height, map_width, map_cell_size,nodeGraph):
        check = False
        while(not check):
            x = randrange(map_width)
            y = randrange(map_height)    

            goal= list(filter(lambda n: n.x == x  and n.y == y, nodeGraph))[0]
            if goal.cellContent is not '#':
                check = True
        
        return goal

    def find_start(self, nodeGraph, bot_index):
        map_cell_size = super().get_map().get_cell_size()
        (last_pos_x, last_pos_y) = self._bots[bot_index].get_saved_pos()
        
        x, y = (last_pos_x // map_cell_size,
                last_pos_y // map_cell_size)
        
        for node in nodeGraph:
            if (node.x == last_pos_x and node.y == last_pos_y):
                return node

        #I think this return is complete mess, avoid an error, must correct it        
        return Node(x,y,"#")
    
    def tick(self, datas):
        result = []

        for bot_index in range(len(self._bots)):
            #Update positions
            (x, y, angle) = datas[bot_index]
            self._bots[bot_index].update(x, y, angle)

            # Get old position and destination
            (last_pos_x, last_pos_y) = self._bots[bot_index].get_saved_pos()
            (dest_x, dest_y) = self._bots[bot_index].get_dest()
            
            #New Astar or continue the one calculated if exist
            if distance(x, y, last_pos_x, last_pos_y) < 3:
                self._bot_set_astar_dest(bot_index, x, y)
                
            elif distance(x, y, dest_x, dest_y) < 30:
                self._bot_set_astar_dest(bot_index, x, y)
            
            #Finally save and move the bots
            self._bots[bot_index].save_pos()
            (dest_x, dest_y) = self._bots[bot_index].get_dest()

            result.append((dest_x, dest_y, 100))

        return result