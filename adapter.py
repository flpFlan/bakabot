# -- stdlib --
import json, logging
from dataclasses import fields
import time
from typing import Optional, TypeVar, TYPE_CHECKING

# -- third party --
from websockets.client import connect
from aiohttp import ClientSession

# -- own --
from cqhttp.events.base import CQHTTPEvent

# -- code --
if TYPE_CHECKING:
    from cqhttp.api.base import ApiAction, ResponseBase

    _TResponse = TypeVar("_TResponse", bound=ResponseBase)

log = logging.getLogger("bot.cqhttp")


class CQHTTPAdapter:
    def __init__(self):
        from accio import ACCIO

        self.endpoint = ACCIO.conf.get("Bot.Adapter", "endpoint")
        self.client = ClientSession()

    async def run(self, host: str, port=2333):
        from accio import ACCIO

        async with connect(f"ws://{host}:{port}/event", ping_timeout=None) as conn:
            self.event = conn
            await ACCIO.bot.behavior.evt_loop()

    async def rev_raw(self):
        return await self.event.recv()

    async def rev_json(self) -> dict:
        raw = await self.rev_raw()
        return json.loads(raw)

    async def rev_evt(self) -> CQHTTPEvent:
        json = await self.rev_json()
        return self.trans_json_to_evt(json)

    async def api(self, act: "ApiAction[_TResponse]") -> "_TResponse":
        params = self.trans_action_to_json(act)
        return await self._api(**params)

    async def _api(self, action: str, echo: Optional[str] = None, **params):
        form = {}
        form["action"] = action
        if params:
            form["params"] = dict(**params)
        if echo:
            form["echo"] = echo

        result = await self.client.post(self.endpoint, json=form)
        print(time.time())
        return await result.json()

    @staticmethod
    def trans_json_to_evt(rev: dict) -> CQHTTPEvent:
        pt = rev.get("post_type")
        assert pt
        tt = rev.get(pt + "_type", " ")
        st = rev.get("sub_type", " ")

        evt = CQHTTPEvent.classes[pt][tt][st](rev)
        return evt

    @staticmethod
    def trans_action_to_json(act: "ApiAction") -> dict:
        fs = map(lambda x: x.name, fields(act))
        result = {}
        for name, value in act.__dict__.items():
            if not name in fs:
                continue
            if isinstance(value, list):
                l = []
                for sub_value in value:
                    r = CQHTTPAdapter.trans_action_to_json(sub_value)
                    l.append(r)
                result[name] = l
            else:
                result[name] = value
        action = getattr(act, "action", None)
        result["action"] = action
        return result