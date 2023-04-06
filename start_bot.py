# -- stdlib --
import asyncio

# -- third party --
# -- own --
from config import Bots, Endpoints

# -- code --


async def start_bot():
    default = {"event": "localhost:2333", "api": "localhost:2334"}
    for bot in Bots:
        evt = Endpoints.get(bot.name, default).get("event")
        api = Endpoints.get(bot.name, default).get("api")

        assert evt and api
        await bot.run(evt, api)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_bot())
    asyncio.get_event_loop().run_forever()
