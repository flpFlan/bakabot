# -- stdlib --
import asyncio, logging

# -- third party --
# -- own --
from config import _Bot_ as bot, Endpoint

# -- code --
logging.basicConfig(
    filename="log.txt",
    format="%(asctime)s - %(name)s - %(levelname)s"
    + "\n==============================================\n"
    + "%(message)s",
    level=logging.DEBUG,
)


def start_bot():
    asyncio.run(bot.start_up())
    bot.run(Endpoint["event"])


if __name__ == "__main__":
    start_bot()
