import configparser
import os.path

class Config:
    """
    Handles user configured values and the configuration file.

    Attributes:
        config (__Config) : Singleton for the config file handler.
    """
    class __Config:
        """
        Singleton for the config file handler.

        Attributes:
            parser (ConfigParser) : Used to read from and write to the config file.
            configPath (string) : Location of the config.ini file
        """

        DEFAULT = {
            'Display' : { 
                'Framerate' : 30,
                'ResolutionWidth' : 1280,
                'ResolutionHeight' : 720,
            },
            'Gameplay' : { 
                'TimeRate' : 1,
                'Ruleset' : "Default",
            },
        }

        def __init__(self):
            """
            Initializes the config file parser. If it doesn't exist, creates it and writes default values.
            """

            self.parser = configparser.ConfigParser()

            self.configPath = "config.ini"

            if os.path.isfile(self.configPath):
                
                self.parser.read(self.configPath)

            self.CheckConfig()

            self.Save()

        def Save(self):
            """
            Write the current config in the config file.
            """
            with open(self.configPath, 'w') as configFile:
                self.parser.write(configFile)

        def CheckConfig(self):
            """
            If the config file is missing attributes or sections, fill them with default values.
            """
            for section in self.DEFAULT.keys():
                if not section in self.parser.keys():
                    self.parser[section] = self.DEFAULT[section]
                else:
                    for attribute in self.DEFAULT[section].keys():
                        if not attribute in self.parser[section].keys():
                            self.parser[section][attribute] = str(self.DEFAULT[section][attribute])


    
    config = None

    @staticmethod
    def Initialize():
        """
        Call this method once in the runtime to initialise Config and use it as static.
        """
        if not Config.config:
            Config.config = Config.__Config()

    @staticmethod
    def Framerate():
        """
        Target FPS value in hertz.
        """
        return int(Config.config.parser["Display"]["Framerate"])

    @staticmethod
    def ResolutionWidth():
        """
        Target window Width value in pixels.
        """
        return int(Config.config.parser["Display"]["ResolutionWidth"])

    @staticmethod
    def ResolutionHeight():
        """
        Target window Height value in pixels.
        """
        return int(Config.config.parser["Display"]["ResolutionHeight"])

    @staticmethod
    def TimeRate():
        """
        The time multiplier at which the game occurs.
        """
        return float(Config.config.parser["Gameplay"]["TimeRate"])

    @staticmethod
    def RulesetName():
        """
        The name of the ruleset that should be used for gameplay.
        """
        return Config.config.parser["Gameplay"]["Ruleset"]

    @staticmethod
    def SetConfigValue(section, attribute, value):
        """
        Change the value of an attribute without saving it yet.
        """
        Config.config.parser[section][attribute] = str(value)

    @staticmethod
    def SetConfigValueSave(section, attribute, value):
        """
        Change the value of an attribute and save the config file.
        """
        Config.SetConfigValue(section, attribute, value)
        Config.config.Save()