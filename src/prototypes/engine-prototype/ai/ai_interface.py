class AI:

    def __init__(self, team, number_of_bots, gameMap):
        self._team = team
        self._number_of_bots = number_of_bots
        self._map = gameMap

    
    def tick(self, datas):
        '''
        Must be implemented by challengers.
        Datas => [..., (x, y, angle), ...]  for each bots
        return  [..., (dest_x, dest_y, speed), ...] for each bots
        '''
        pass

    # Getters for children
    def get_team(self):
        return self._team

    def get_number_of_bots(self):
        return self._number_of_bots

    def get_map(self):
        return self._map

    def __repr__(self):
        return "AI({})".format(self._team)
