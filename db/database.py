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

    async def close(self):
        assert self.connection
        self.connection.close()
        self.connection = None
        self.cursor = None

    def execute(self, sql: str, params=None):
        assert self.cursor
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)

    def fatchall(self):
        assert self.cursor
        return self.cursor.fetchall()

    def fatchmany(self, size: int | None = 1):
        assert self.cursor
        return self.cursor.fetchmany(size)

    def fatchone(self):
        assert self.cursor
        return self.cursor.fetchone()

    def commit(self):
        assert self.connection
        self.connection.commit()
