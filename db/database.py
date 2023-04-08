# -- stdlib --
import sqlite3
from typing import cast

# -- third party --
# -- own --
# -- code --


class DataBase:
    def __init__(self, bot):
        from bot import Bot

        self.bot = bot = cast(Bot, bot)

    async def connect(self, db: str = ""):
        db = db or self.bot.name + ".db"
        self.connection = conn = sqlite3.connect(db)
        self.cursor = conn.cursor()

    async def execute(self, sql: str):
        assert self.connection
        self.connection.execute(sql)

    async def commit(self):
        assert self.connection
        self.connection.commit()

    async def close(self):
        assert self.connection
        self.connection.close()
        self.connection = None
        self.cursor = None
