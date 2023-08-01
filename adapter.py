# -- stdlib --
import json, logging,asyncio
from dataclasses import fields
from typing import Optional, TypeVar, TYPE_CHECKING

# -- third party --
from websockets.client import connect

# -- own --
from cqhttp.events.base import CQHTTPEvent
from cqhttp.cqcode.base import CQCode

# -- code --
if TYPE_CHECKING:
    from cqhttp.api.base import ApiAction, ResponseBase

    _TResponse = TypeVar("_TResponse", bound=ResponseBase)

log = logging.getLogger("bot.adapter")


class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, CQCode):
            return o.__str__()
        return super().default(o)


class CQHTTPAdapter:
    def __init__(self):
        from accio import ACCIO

        endpoint = ACCIO.conf.get("Bot.Adapter", "endpoint")
        self.host, self.port = endpoint.split(":")

    async def run(self):
        from accio import ACCIO

        async for conn in connect(
            f"ws://{self.host}:{self.port}/event", ping_timeout=None
        ):
            self.api_conn = await connect(
                f"ws://{self.host}:{self.port}/api", ping_timeout=None
            )
            self.api_lock=asyncio.Lock()
            self.event_conn = conn
            await ACCIO.bot.behavior.evt_loop()
            await self.api_conn.close()

    async def rev_raw(self):
        return await self.event_conn.recv()

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
        async with self.api_lock:
            await self.api_conn.send(json.dumps(form, cls=Encoder))
            result = await self.api_conn.recv()
        return json.loads(result)

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
