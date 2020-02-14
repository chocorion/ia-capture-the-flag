import configparser
import os.path

from service.Config import Config

class Ruleset:
    class __Ruleset:

        DEFAULT = {
            'Default' : { 
                'BotsCount' : 5,
            },
        }

        def __init__(self):
            self.parser = configparser.ConfigParser()

            self.filePath = "rulesets.ini"

            if not os.path.isfile(self.filePath):

                self.SaveDefault()

            else:
                
                self.parser.read(self.filePath)

                self.CheckRuleset()

                self.Save()

        def Save(self):
            with open(self.filePath, 'w') as configFile:
                self.parser.write(configFile)

        def SaveDefault(self):
            # Default config values
            self.CheckRuleset()

            self.Save()

        def CheckRuleset(self):
            for section in self.DEFAULT.keys():
                if not section in self.parser.keys():
                    self.parser[section] = self.DEFAULT[section]
                else:
                    for attribute in self.DEFAULT[section].keys():
                        if not attribute in self.parser[section].keys():
                            self.parser[section][attribute] = str(self.DEFAULT[section][attribute])


    
    rulesets = None

    @staticmethod
    def Initialize():
        if not Ruleset.rulesets:
            Ruleset.rulesets = Ruleset.__Ruleset()

    @staticmethod
    def GetRuleset():
        return Ruleset.rulesets.parser[Config.RulesetName()]

    @staticmethod
    def GetRulesetValue(attribute):
        return Ruleset.rulesets.parser[Config.RulesetName()][attribute]

    @staticmethod
    def SetRulesetValue(attribute, value):
        Ruleset.rulesets.parser[Config.RulesetName()][attribute] = str(value)

    @staticmethod
    def SetRulesetValueSave(attribute, value):
        Ruleset.SetRulesetValue(attribute, value)
        Ruleset.rulesets.Save()