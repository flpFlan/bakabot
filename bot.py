# -- stdlib --
import asyncio, logging, json, re
from typing import cast

# -- third party --
from websockets.server import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosed

# -- own --
from backend import Backend, ApiBackEnd
from revprocessor import revProcessor


# -- code --
log = logging.getLogger("Bot")


class Bot:
    running: bool = False
    services = []
    backend: Backend
    api_server: ApiBackEnd
    _ = {}

    def __init__(self, name: str, qq_number: int):
        self.name = name
        self.qq_number = qq_number
        self.rev_processor = revProcessor(self)

    async def run(self, evt_host: str, evt_port: int, api_host: str, api_port: int):
        self.backend = getattr(self, "backend", None) or Backend(self)
        self.api_server = getattr(self, "api_server", None) or ApiBackEnd(self)
        await self.backend.serve(evt_host, evt_port)
        await self.api_server.serve(api_host, api_port)

        for s in self.services:
            s.entry = s.entry or []
            s.entry = [re.compile(e, s.entry_flags or 0) for e in s.entry]
            s.start()

        self.running = True

    def close(self):
        self.backend.close()
        self.api_server.close()
        self.running = False

    async def main_loop(self, ws: WebSocketServerProtocol, path: str):
        self.backend.go = ws

        while True:
            try:
                rev = await self.rev()
            except ConnectionClosed:
                self.running = False
                log.debug("bot shootdown")
                break

            if not rev:
                continue
            post_type = rev.get("post_type")
            process_result = self.rev_processor.process_by_type(post_type, rev)
            print(process_result)
            handlers = list(filter(lambda s: post_type in s.category, self.services))

            if not handlers:
                continue
            if post_type == "message":
                ...
            if post_type == "notice":
                ...
            if post_type == "request":
                ...
            if post_type == "redbag":
                ...

    async def rev(self) -> dict:
        raw_msg = await self.backend.rev_raw()
        return msg_to_json(raw_msg)

    async def send_group_msg(self, msg, group_id=None):
        ...

    async def api_server_loop(self, ws: WebSocketServerProtocol, path: str):
        self.api_server.go = ws
        while not self.api_server.go.closed:
            await asyncio.sleep(1)
        self.api_server.go = cast(WebSocketServerProtocol, None)

    async def api(self, action: str, echo: str = "", **params) -> dict:
        if not self.api_server.go:
            log.error("api connection not exists")
            return {"error": "api connection not exists"}
        form = {}
        form["action"] = action
        if params:
            form["params"] = dict(**params)
        if echo:
            form["echo"] = echo

        await self.api_server.send(json.dumps(form))
        result = await self.api_server.rev_raw()

        return msg_to_json(result)


def msg_to_json(msg: str) -> dict:
    # for i in msg:
    #   if i == "{" and msg[-1] == "\n":
    #       return json.loads(msg[i:])
    # return {"error": msg}
    return json.loads(msg)
