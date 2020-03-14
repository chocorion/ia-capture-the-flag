from model.ArgBuilder.ArgBuilder import ArgBuilder
from service.Ruleset import Ruleset

class DictBuilder(ArgBuilder):
    
    def getResult(self):
        """
        Return the argument built by this builder.

        Return :
            dico (dict()) : Dict containing all the arguments.
        """
        if self._finished:
            return self._dico
        
        raise Exception("Object was not completed !")


    def beginArgument(self):
        self._dico = { "bots" : {}, "events" : {}}
        self._currentBotId = 0

        self._finished = False


    def endArgument(self):
        if self._currentBotId != int(Ruleset.GetRulesetValue("BotsCount")):
            raise Exception("Argument doesn't contain 5 bots !")

        self._finished = True


    def addBot(self, bot, botId):
        if self._currentBotId >= int(Ruleset.GetRulesetValue("BotsCount")):
            raise Exception("To many bots in this argument")
        
        self._dico["bots"][botId] = {
            "currentPosition" : (bot.x, bot.y, bot.angle, bot.speed),
            "life": bot.health,
            "flag": bot.flag(),
            "cooldown": bot.cooldown()
        }
        self._currentBotId += 1


    def addFlag(self, team, currentPosition):
        if "flags" not in self._dico["events"].keys():
            self._dico["events"]["flags"] = list()

        self._dico["events"]["flags"].append({"team": team, "position": (currentPosition[0], currentPosition[1])})

    def addMissedTicks(self, missedTicks):
        self._dico["missedTicks"] = missedTicks