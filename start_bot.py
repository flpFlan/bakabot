# -- stdlib --
import asyncio

# -- third party --
# -- own --
from config import Bots, Endpoints

# -- code --


async def start_bot():
    default = "localhost:2333"
    for bot in Bots:
        addr = Endpoints.get(bot.name, default)

        assert addr
        await bot.run(addr)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_bot())
    asyncio.get_event_loop().run_forever()
