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


    def add_bot(self, bot):
        if self._current_bot_id >= int(Ruleset.GetRulesetValue("BotsCount")):
            raise Exception("To many bots in this argument")
        
        bot_identifier = str(bot.player) + "_" + str(self._current_bot_id)
        
        self._dico["bots"][bot_identifier] = {
            "current_position" : (bot.x, bot.y, bot.angle, bot.speed),
            "life": bot.health,
            "flag": bot.flag(),
            "cooldown": bot.cooldown()
        }
        self._current_bot_id += 1
