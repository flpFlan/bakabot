# -- stdlib --
import os

# -- third party --
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

# -- own --
# -- code --


class Model(AsyncAttrs, DeclarativeBase):
    pass


class DataBase:
    def __init__(self):
        if not os.path.exists("src/db"):
            os.makedirs("src/db")
        from accio import ACCIO

        self.engine = create_async_engine(
            f"sqlite+aiosqlite:///src/db/{ACCIO.bot.name}.sqlite3"
        )
        self.session = async_sessionmaker(self.engine, expire_on_commit=False)()

    async def setup(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Model.metadata.create_all)
