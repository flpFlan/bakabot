# -- stdlib --
import json, logging, asyncio
from typing import cast
from urllib.parse import urljoin
from collections import defaultdict

# -- third party --
from websockets.client import connect
from websockets.exceptions import ConnectionClosed
from tenacity import retry, wait_fixed, stop_after_attempt

# -- own --
from options import MAX_CONNECT_RETRIES
from cqhttp.events.base import CQHTTPEvent
from cqhttp.events.base import all_events
from cqhttp.api.base import ApiAction

# -- code --
log = logging.getLogger("bot.go")


async def _callback(x):
    bot = x.args[0].bot
    await bot.stop()
    log.error("max retry reached, %sshootdown", bot.name)
    raise Exception("Max Retry Reached")


class CQHTTPAdapter:
    def __init__(self, bot):
        from bot import Bot

        self.bot = bot = cast(Bot, bot)

    @retry(
        wait=wait_fixed(1),
        stop=stop_after_attempt(MAX_CONNECT_RETRIES),
        retry_error_callback=lambda x: asyncio.ensure_future(_callback(x)),
    )
    async def connect(self, uri: str):
        self.evt_connection = await connect(urljoin(uri, "/event"), ping_interval=None)
        self.api_uri = urljoin(uri, "/api")

    async def disconnect(self):
        await self.evt_connection.close()

    async def rev_raw(self) -> str:
        try:
            raw = await self.evt_connection.recv()
        except ConnectionClosed:
            log.warning("event connection shootdown,attempting to reconnect...")
            host, port = self.evt_connection.host, self.evt_connection.port
            assert host and port
            await self.connect(f"{host}:{port}")
            raw = await self.evt_connection.recv()
        return cast(str, raw)

    async def rev_json(self) -> dict:
        raw = await self.rev_raw()
        return json.loads(raw)

    async def rev_evt(self) -> CQHTTPEvent:
        json = await self.rev_json()
        return self.trans_json_to_evt(json)

    async def api(self, act: ApiAction) -> bool:
        params = self.trans_action_to_json(act)
        result = await self._api(**params)
        if res := act.response:
            set_attr(res, result)
        if result.get("status", "failed") == "failed":
            log.info(f"api call failed:\n{result}")
            return False
        return True

    async def _api(self, action: str, echo="", **params) -> dict:  # type: ignore
        form = {}
        form["action"] = action
        if params:
            form["params"] = dict(**params)
        if echo:
            form["echo"] = echo

        data = json.dumps(form)
        loop = asyncio.get_event_loop()
        if not (lock := getattr(loop, "api_lock", None)):
            lock = asyncio.Lock()
            setattr(loop, "api_lock", lock)
        async with connect(self.api_uri) as api_connection:
            try:
                await api_connection.send(data)
                result = await api_connection.recv()
            except ConnectionClosed:
                log.warning("api connection shootdown")
                raise Exception("api connection shootdown")
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
        result = {}
        for name, value in act.__dict__.items():
            if name in ("bot", "_", "response", "_callback"):
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


class P_CQHTTPAdapter(CQHTTPAdapter):
    def __init__(self, bot):
        super().__init__(bot)
        import requests

        self.session = requests.Session()

    @retry(
        wait=wait_fixed(1),
        stop=stop_after_attempt(MAX_CONNECT_RETRIES),
        retry_error_callback=lambda x: asyncio.run(_callback(x)),
    )
    async def connect(self, evt_uri: str, api_uri: str):
        self.evt_connection = await connect(
            urljoin(evt_uri, "/event"), ping_interval=None
        )
        self.api_uri = api_uri

    async def _api(self, action: str, echo="", **params) -> dict:
        form = {}
        form["action"] = action
        if params:
            form["params"] = dict(**params)
        if echo:
            form["echo"] = echo

        data = json.dumps(form)
        r = self.session.post(self.api_uri, json=data)
        r.raise_for_status()
        return r.json()
