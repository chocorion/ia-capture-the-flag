from model.ArgBuilder import ArgBuilder

class DictBuilder(ArgBuilder):
    
    def get_result(self):
        """
        Return the argument built by this builder.

        Return :
            dico (dict()) : Dict containing all the arguments.
        """
        if self._finish:
            return self._dico
        
        raise Exception("Object was not completed !")


    def begin_argument(self):
        self._dico = dict()
        self._current_bot_id = 0

        self._finish = False


    def end_argument(self):
        if self._current_bot_id != 5:
            raise Exception("Argument doesn't contain 5 bots !")

        self._finish = True


    def add_bot(self):
        if self._current_bot_id >= 5:
            raise Exception("To much bot in this argument")

        self._current_bot_id += 1
        self._dico[self._current_bot_id] = dict()


    def add_life(self, life_amount):
        self._dico[self._current_bot_id]["life"] = life_amount


    def add_flag(self, flag_num):
        self._dico[self._current_bot_id]["flag"] = flag_num


    def add_cooldown(self, cooldown_millis):
        self._dico[self._current_bot_id]["cooldown"] = cooldown_millis 