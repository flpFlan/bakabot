# -- stdlib --
import asyncio, logging

# -- third party --
# -- own --
from config import Bots, Endpoints

# -- code --
logging.basicConfig(
    filename="log.txt",
    format="%(asctime)s - %(name)s - %(levelname)s"
    + "\n==============================================\n"
    + "%(message)s",
    level=logging.DEBUG,
)


async def start_bot():
    default = "localhost:2333"
    for bot in Bots:
        addr = Endpoints.get(bot.name, default)

        assert addr
        await bot.behavior.run(addr)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_bot())
    asyncio.get_event_loop().run_forever()
