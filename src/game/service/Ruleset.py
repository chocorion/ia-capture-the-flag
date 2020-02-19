import configparser
import os.path

from service.Config import Config

class Ruleset:
    """
    This class is highly similar to Config. Please refer to it when missing.

    Attributes:
        rulesets (__Ruleset) : Singleton for the rulesets file handler.
    """
    class __Ruleset:

        DEFAULT = {
            'Default' : { 
                'BotsCount' : 5,
                'SpeedMultiplier' : 1,
                'RotationMultiplier' : 1,
                'StartCountdownSeconds' : 5,
                'ThinkTimeMs' : 16,
            },
        }

        def __init__(self):
            """
            Initializes the rulesets file parser. If it doesn't exist, creates it and writes default values.
            """
            self.parser = configparser.ConfigParser()

            self.filePath = "rulesets.ini"

            if os.path.isfile(self.filePath):
                
                self.parser.read(self.filePath)

            self.CheckRuleset()

            self.Save()

        def Save(self):
            """
            Write the current rulesets in the rulesets file.
            """
            with open(self.filePath, 'w') as configFile:
                self.parser.write(configFile)

        def CheckRuleset(self):
            """
            If the rulesets file is missing attributes or sections, fill them with default values.
            """
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
        """
        The entire definition of the currently selected ruleset.
        """
        return Ruleset.rulesets.parser[Config.RulesetName()]

    @staticmethod
    def GetRulesetValue(attribute):
        """
        Any attribute in the currently selected ruleset.
        """
        return Ruleset.rulesets.parser[Config.RulesetName()][attribute]

    @staticmethod
    def SetRulesetValue(attribute, value):
        Ruleset.rulesets.parser[Config.RulesetName()][attribute] = str(value)

    @staticmethod
    def SetRulesetValueSave(attribute, value):
        Ruleset.SetRulesetValue(attribute, value)
        Ruleset.rulesets.Save()