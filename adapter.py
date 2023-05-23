# -- stdlib --
import json, logging
from dataclasses import fields, is_dataclass
from types import NoneType
from typing import Optional, get_args

# -- third party --
from quart import Quart, websocket

# -- own --
from cqhttp.events.base import CQHTTPEvent
from cqhttp.api.base import ApiAction
from utils.algorithm import first

# -- code --
log = logging.getLogger("bot.cqhttp")


class CQHTTPAdapter:
    Adapter = Quart(__name__)

    def run(self, host="0.0.0.0", port=2333):
        self.Adapter.run(host, port)

    async def shutdown(self):
        await self.Adapter.shutdown()

    async def rev_raw(self) -> str:
        return await websocket.receive()

    async def rev_json(self) -> dict:
        raw = await self.rev_raw()
        return json.loads(raw)

    async def rev_evt(self) -> CQHTTPEvent:
        json = await self.rev_json()
        return self.trans_json_to_evt(json)

    async def api(self, act: ApiAction) -> dict:
        params = self.trans_action_to_json(act)
        return await self._api(**params)

    async def _api(self, action: str, echo: Optional[str] = None, **params) -> dict:
        form = {}
        form["action"] = action
        if params:
            form["params"] = dict(**params)
        if echo:
            form["echo"] = echo

        data = json.dumps(form)
        await websocket.send(data)
        result = await websocket.receive()
        return json.loads(result)

    @staticmethod
    def trans_json_to_evt(rev: dict) -> CQHTTPEvent:
        pt = rev.get("post_type")
        assert pt
        tt = rev.get(pt + "_type", " ")
        st = rev.get("sub_type", " ")

        evt = CQHTTPEvent.classes[pt][tt][st]
        params = {k: v for k, v in get_kwargs(evt, rev)}
        return evt(**params)

    @staticmethod
    def trans_action_to_json(act: ApiAction) -> dict:
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


def get_kwargs(evt: CQHTTPEvent, json: dict):
    for f in fields(evt):
        name, type = f.name, f.type
        if ts := get_args(type):
            type = first(ts, lambda x: x is not NoneType)
            assert type
        if is_dataclass(type):
            args = {k: v for k, v in get_kwargs(type, json[name])}
            value = type(**args)
        else:
            value = json[name]
        yield name, value


def set_attr(obj, attrs: dict):
    for name, value in attrs.items():
        if isinstance(value, dict):
            sub_obj = obj.__annotations__.get(name)
            if args := getattr(sub_obj, "__args__", None):
                sub_obj = args[0]
            sub_obj = sub_obj()
            set_attr(sub_obj, value)
            setattr(obj, name, sub_obj)
        elif isinstance(value, list):
            l = []
            for i in value:
                if isinstance(i, dict):
                    o = obj.__annotations__.get(name, object).__args__[0]()
                    set_attr(o, i)
                    l.append(o)
                else:
                    l.append(i)
            setattr(obj, name, l)

        else:
            setattr(obj, name, value)


# TODO
# async def _callback(x):
#     bot = x.args[0].bot
#     await bot.stop()
#     log.error("max retry reached, %sshootdown", bot.name)
#     raise Exception("Max Retry Reached")


# class P_CQHTTPAdapter(CQHTTPAdapter):
#     def __init__(self):
#         super().__init__()
#         import requests

#         self.session = requests.Session()

#     @retry(
#         wait=wait_fixed(1),
#         stop=stop_after_attempt(MAX_CONNECT_RETRIES),
#         retry_error_callback=lambda x: asyncio.run(_callback(x)),
#     )
#     async def connect(self, evt_uri: str, api_uri: str):
#         self.evt_connection = await connect(
#             urljoin(evt_uri, "/event"), ping_interval=None
#         )
#         self.api_uri = api_uri

#     async def _api(self, action: str, echo="", **params) -> dict:
#         form = {}
#         form["action"] = action
#         if params:
#             form["params"] = dict(**params)
#         if echo:
#             form["echo"] = echo

#         data = json.dumps(form)
#         r = self.session.post(self.api_uri, json=data)
#         r.raise_for_status()
#         return r.json()
