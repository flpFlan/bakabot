# -- stdlib --
import json
from typing import cast
from urllib.parse import urljoin

# -- third party --
from websockets.client import connect

# -- own --
from bot import Bot

# -- code --


class CQHTTPAdapter:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def connect(self, evt_uri: str, api_uri: str):
        self.evt_connection = await connect(urljoin(evt_uri, "/event"))
        self.api_connection = await connect(urljoin(api_uri, "/api"))

    async def disconnect(self):
        await self.evt_connection.close()
        await self.api_connection.close()

    async def rev_raw(self) -> str:
        raw = await self.evt_connection.recv()
        return cast(str, raw)

    async def rev(self) -> dict:
        raw = await self.rev_raw()
        return json.loads(raw)

    async def post_api(self, action: str, echo="", **params) -> dict:
        form = {}
        form["action"] = action
        if params:
            form["params"] = dict(**params)
        if echo:
            form["echo"] = echo

        await self.api_connection.send(form)

        result = await self.api_connection.recv()
        return json.loads(result)
