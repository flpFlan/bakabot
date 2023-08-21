# -- stdlib --
from configparser import ConfigParser

# -- own --
# -- code --


class Accio:
    __slots__ = ("bot", "db", "conf")

    def __init__(self):
        # config
        conf = ConfigParser()
        conf.read("config.ini")
        self.conf = conf

        # bot
        from bot import Bot

        name = conf.get("Bot", "name")
        qq = conf.getint("Bot", "qq")
        self.bot = Bot(name, qq)

        # database
        from db.database import DataBase

        self.db = DataBase()
        self.db.set_bot(self.bot)
