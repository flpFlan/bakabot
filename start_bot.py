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
        # RotatingFileHandler("bakabot.log", maxBytes=1024 * 1024 * 5, backupCount=3),
    ],
)


async def start_bot():
    bot = ACCIO.bot
    await bot.install_services()
    # import argparse

    # parser = argparse.ArgumentParser(prog=sys.argv[0])
    # parser.add_argument("--host", default="localhost", type=str)
    # parser.add_argument("--port", default="2333", type=int)
    # options = parser.parse_args()

    import logging
    logging.getLogger("bot").info(f"{ACCIO.bot.name} start up!")
    await bot.run_forever()


if __name__ == "__main__":
    try:
        import uvloop

        loop = uvloop.new_event_loop()
    except ImportError:
        loop = None

    with asyncio.Runner(loop_factory=loop) as runner:
        runner.run(start_bot())
