# -- stdlib --
import asyncio, logging
import sys

# -- third party --
# -- own --
from accio import ACCIO

# -- code --
logging.basicConfig(
    format="""
    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    %(asctime)s - %(name)s - %(levelname)s
    %(message)s
    <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    """,
    level=logging.INFO,
    handlers=[logging.StreamHandler(), logging.FileHandler("log.txt")],
)


def start_bot():
    bot = ACCIO.bot
    asyncio.run(bot.set_up())
    import argparse

    parser = argparse.ArgumentParser(prog=sys.argv[0])
    parser.add_argument("--host", default="localhost", type=str)
    parser.add_argument("--port", default="2333", type=int)
    options = parser.parse_args()

    bot.run(options.host, options.port)


if __name__ == "__main__":
    start_bot()
