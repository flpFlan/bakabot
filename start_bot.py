# -- stdlib --
import asyncio, logging
from logging.handlers import RotatingFileHandler
import sys

# -- own --
from accio import ACCIO

# -- code --
logging.basicConfig(
    format="""
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[%(asctime)s] - [%(name)s] - [%(levelname)s]
%(message)s
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
""",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        RotatingFileHandler("bakabot.log", maxBytes=1024 * 1024 * 5, backupCount=3),
    ],
)


async def start_bot():
    bot = ACCIO.bot
    await bot.setup()
    # import argparse

    # parser = argparse.ArgumentParser(prog=sys.argv[0])
    # parser.add_argument("--host", default="localhost", type=str)
    # parser.add_argument("--port", default="2333", type=int)
    # options = parser.parse_args()

    await bot.run_forever()


if __name__ == "__main__":
    with asyncio.Runner() as runner:
        runner.run(start_bot())
