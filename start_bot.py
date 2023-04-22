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


async def start_bot(loop):
    default = "localhost:2333"
    for bot in Bots:
        addr = Endpoints.get(bot.name, default)
        await bot.start_up(addr)
        loop.create_task(bot.behavior.loop(loop))


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(start_bot(loop))
    loop.run_forever()
