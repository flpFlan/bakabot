# -- stdlib --
from configparser import ConfigParser

# -- own --
from bot import Bot
from db.database import DataBase

# -- code --


class Accio:
    def __init__(self):
        # config
        conf = ConfigParser()
        conf.read("config.ini")
        self.conf = conf

        # bot
        name = conf.get("Bot", "name")
        qq = conf.getint("Bot", "qq")
        self.bot = Bot(name, qq)

        # database
        self.db = DataBase()
        self.db.set_bot(self.bot)
