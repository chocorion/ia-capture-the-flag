from model.ArgBuilder import ArgBuilder

class DictBuilder(ArgBuilder):
    
    def get_result(self):
        if self._finish:
            return self._dico
        
        raise Exception("Object was not completed !")

    def begin_argument(self):
        self._dico = dict()
        self._current_bot_id = 0
        
        self._finish = False

    def end_argument(self):


    def add_bot(self):

    def add_life(self):

    def add_flag(self):

    def add_cooldown(self):