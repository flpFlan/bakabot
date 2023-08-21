# -- third party --
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

# -- own --
# -- code --

class DataBase:
    def __init__(self):
        self.engine = create_async_engine("sqlite+aiosqlite:///db.sqlite", echo=True)