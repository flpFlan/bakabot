# -- stdlib --
from configparser import ConfigParser
from typing import TYPE_CHECKING

# -- own --
from bot import Bot
from db.database import DataBase

# -- code --

if TYPE_CHECKING:
    from cqhttp.cqcode.cqcode import Image, Record

class Accio:
    
    def __init__(self):
        # config
        conf=ConfigParser()
        conf.read("config.ini")
        self.conf=conf

        # bot
        name=conf.get("Bot","name")
        qq=conf.getint("Bot","qq")
        self.bot=Bot(name,qq)

        # database
        self.db=DataBase()
        self.db.set_bot(self.bot)

        def __setattr__(__name, __value):
            raise Exception("you can't change any property of ACCIO!!")
        
        self.__setattr__=__setattr__

    # method

    def sgm(self, msg: str, group_id: int):
        ...

    def spm(self, msg, qq: int):
        ...

    def image(self, img: Image, group_id: int):
        ...

    def record(self, record: Record, group_id: int):
        ...

    def segm(self):
        ...

    def sfgm(self):
        ...


ACCIO = Accio()
