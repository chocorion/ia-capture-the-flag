from model.ArgBuilder.ArgBuilder import ArgBuilder
from model.ArgBuilder.DictBuilder import DictBuilder
from service.Ruleset import Ruleset

import json

class JSONBuilder(ArgBuilder):
    
    def getResult(self):
        """
        Return the argument built by this builder.

        Return :
            json (string) : string in JSON format
        """
        return json.dumps(self._dictBuilder.getResult())


    def beginArgument(self):
        self._dictBuilder = DictBuilder()
        self._dictBuilder.beginArgument()


    def endArgument(self):
        self._dictBuilder.endArgument()


    def addBot(self, bot, botId, seen):
        self._dictBuilder.addBot(bot, botId, seen)


    def addMissedTicks(self, missedTicks):
        self._dictBuilder.addMissedTicks(missedTicks)