from model.ArgBuilder.ArgBuilder import ArgBuilder
from model.ArgBuilder.DictBuilder import DictBuilder
from service.Ruleset import Ruleset

import json

class JSONBuilder(ArgBuilder):
    
    def get_result(self):
        """
        Return the argument built by this builder.

        Return :
            json (string) : string in JSON format
        """
        return json.dumps(self._dictBuilder.get_result())


    def begin_argument(self):
        self._dictBuilder = DictBuilder()
        self._dictBuilder.begin_argument()


    def end_argument(self):
        self._dictBuilder.end_argument()


    def add_bot(self, bot):
        self._dictBuilder.add_bot(bot)