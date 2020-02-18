from model.ArgBuilder import ArgBuilder
from service.Ruleset import Ruleset

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
        if self._current_bot_id != int(Ruleset.GetRulesetValue("BotsCount")):
            raise Exception("Argument doesn't contain 5 bots !")

        self._finish = True


    def add_bot(self, life_amount, flag_number, cooldown):
        if self._current_bot_id >= int(Ruleset.GetRulesetValue("BotsCount")):
            raise Exception("To much bot in this argument")

        self._current_bot_id += 1
        self._dico[self._current_bot_id] = {
            "life": life_amount,
            "flag": flag_number,
            "cooldown": cooldown
        }