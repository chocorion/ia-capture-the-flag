import configparser
import os.path

class Config:
    class __Config:

        DEFAULT = {
            'Display' : { 
                'Framerate' : 30,
            }
        }

        def __init__(self):
            self.parser = configparser.ConfigParser()

            self.configPath = "config.ini"

            if not os.path.isfile(self.configPath):

                self.SaveDefault()

            else:
                
                self.parser.read(self.configPath)

                self.CheckConfig()

                self.Save()

        def Save(self):
            with open(self.configPath, 'w') as configFile:
                self.parser.write(configFile)

        def SaveDefault(self):
            # Default config values
            self.CheckConfig()

            self.Save()

        def CheckConfig(self):
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
        if not Config.config:
            Config.config = Config.__Config()

    @staticmethod
    def Framerate():
        return int(Config.config.parser["Display"]["Framerate"])

    @staticmethod
    def SetConfigValue(section, attribute, value):
        Config.config.parser[section][attribute] = str(value)

    @staticmethod
    def SetConfigValueSave(section, attribute, value):
        Config.SetConfigValue(section, attribute, value)
        Config.config.Save()