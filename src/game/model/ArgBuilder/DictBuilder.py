from model.ArgBuilder.ArgBuilder import ArgBuilder
from service.Ruleset import Ruleset

class DictBuilder(ArgBuilder):
    
    def get_result(self):
        """
        Return the argument built by this builder.

        Return :
            dico (dict()) : Dict containing all the arguments.
        """
        if self._finished:
            return self._dico
        
        raise Exception("Object was not completed !")


    def begin_argument(self):
        self._dico = { "bots" : {}, "events" : {}}
        self._current_bot_id = 0

        self._finished = False


    def end_argument(self):
        if self._current_bot_id != int(Ruleset.GetRulesetValue("BotsCount")):
            raise Exception("Argument doesn't contain 5 bots !")

        self._finished = True


    def add_bot(self, bot, bot_id):
        if self._current_bot_id >= int(Ruleset.GetRulesetValue("BotsCount")):
            raise Exception("To many bots in this argument")
        
        self._dico["bots"][bot_id] = {
            "current_position" : (bot.x, bot.y, bot.angle, bot.speed),
            "life": bot.health,
            "flag": bot.flag(),
            "cooldown": bot.cooldown()
        }
        self._current_bot_id += 1


    def add_flag(self, team, current_position):
        if "flags" not in self._dico["events"].keys():
            self._dico["events"]["flags"] = list()

        self._dico["events"]["flags"].append({"team": team, "position": (current_position[0], current_position[1])})
