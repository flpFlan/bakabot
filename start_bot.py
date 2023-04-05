# -- stdlib --
import asyncio

# -- third party --
# -- own --
from config import Bots, Endpoints

# -- code --


async def start_bot():
    default = {
        "evt_host": "localhost",
        "evt_port": 2333,
        "api_host": "localhost",
        "api_port": 2334,
    }
    for bot in Bots:
        await bot.run(**Endpoints.get(bot.name, default))


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_bot())
    asyncio.get_event_loop().run_forever()
