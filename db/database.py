# -- stdlib --
import aiosqlite
from typing import TYPE_CHECKING

# -- code --
if TYPE_CHECKING:
    from bot import Bot


class DataBase:
    def set_bot(self, bot: "Bot"):
        self.bot = bot

    async def connect(self, db: str = ""):
        db = db or self.bot.name + ".db"
        self.connection = conn = await aiosqlite.connect(db)
        self.cursor = await conn.cursor()

    async def close(self):
        assert self.connection
        await self.connection.close()

    async def execute(self, sql: str, params=None):
        assert self.cursor
        if params:
            await self.cursor.execute(sql, params)
        else:
            await self.cursor.execute(sql)
        await self.commit()

    async def fatchall(self):
        assert self.cursor
        return await self.cursor.fetchall()

    async def fatchmany(self, size: int | None = 1):
        assert self.cursor
        return await self.cursor.fetchmany(size)

    async def fatchone(self):
        assert self.cursor
        return await self.cursor.fetchone()

    async def commit(self):
        assert self.connection
        await self.connection.commit()
