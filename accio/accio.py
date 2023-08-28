# -- stdlib --
from configparser import ConfigParser

# -- own --
# -- code --


class Accio:
    __slots__ = ("bot", "db", "conf")

    def load_config(self):
        conf = ConfigParser()
        conf.read("config.ini")
        self.conf = conf
        return conf

    def setup(self):
        conf = self.load_config()
        # src
        import os
        
        if not os.path.exists("src/temp"):
            os.makedirs("src/temp")

        # bot
        from bot import Bot

        name = conf.get("Bot", "name")
        qq = conf.getint("Bot", "qq")
        self.bot = Bot(name, qq)

        # database
        from db.base import DataBase

        self.db = DataBase()
