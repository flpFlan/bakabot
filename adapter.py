# -- stdlib --
import json, logging
from typing import cast, TypeVar
from urllib.parse import urljoin

# -- third party --
from websockets.client import connect
from websockets.exceptions import ConnectionClosedError

# -- own --
from cqhttp.events.base import CQHTTPEvent
from cqhttp.events.base import all_events
from cqhttp.api.base import ApiAction, all_apis

# -- code --
log = logging.getLogger("bot")
# T = TypeVar("T", *all_apis)


class CQHTTPAdapter:
    def __init__(self, bot):
        from bot import Bot

        self.bot = bot = cast(Bot, bot)

    async def connect(self, uri: str):
        self.evt_connection = await connect(urljoin(uri, "/event"))
        self.api_connection = await connect(urljoin(uri, "/api"))

    async def disconnect(self):
        await self.evt_connection.close()
        await self.api_connection.close()

    async def rev_raw(self) -> str:
        try:
            raw = await self.evt_connection.recv()
        except ConnectionClosedError:
            log.error("go-cqhttp connection shootdown")
            await self.connect("ws://localhost:2333")
            return await self.rev_raw()
        return cast(str, raw)

    async def rev_json(self) -> dict:
        raw = await self.rev_raw()
        return json.loads(raw)

    async def rev_evt(self) -> CQHTTPEvent:
        json = await self.rev_json()
        return self.trans_json_to_evt(json)

    async def api(self, act: ApiAction):
        params = self.trans_action_to_json(act)
        result = await self._api(**params)
        if act.Response is ApiAction.Response:
            return
        res = act.Response()
        set_attr(res, result)
        return res

    async def _api(self, action: str, echo="", **params) -> dict:
        form = {}
        form["action"] = action
        if params:
            form["params"] = dict(**params)
        if echo:
            form["echo"] = echo

        try:
            await self.api_connection.send(form)
        except ConnectionClosedError:
            log.error("go-cqhttp connection shootdown")
            await self.connect("ws://localhost:2333")
            await self.api_connection.send(form)
        result = await self.api_connection.recv()

        return json.loads(result)

    @staticmethod
    def trans_json_to_evt(rev: dict) -> CQHTTPEvent:
        pt = rev.get("post_type")
        assert pt
        tt = rev.get(pt + "_type", " ")
        st = rev.get("sub_type", " ")

        evt = all_events[pt][tt][st]()
        assert evt

        set_attr(evt, rev)
        return evt

    @staticmethod
    def trans_action_to_json(act: ApiAction) -> dict:
        return act.__dict__


def set_attr(obj, attrs: dict):
    for name, value in attrs.items():
        if not isinstance(value, dict):
            setattr(obj, name, value)
        else:
            sub_obj = obj.__annotations__.get(name)
            assert sub_obj
            set_attr(sub_obj(), value)
