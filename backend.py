# -- stdlib --
from typing import cast

# -- third party --
from websockets.server import serve, WebSocketServerProtocol

# -- own --


# -- code --


class Backend:
    go: WebSocketServerProtocol

    def __init__(self, bot):
        self.bot = bot

    async def serve(self, host, port):
        self.endpoint = await serve(self.bot.main_loop, host, port)

    async def rev_raw(self) -> str:
        assert self.go

        raw_msg = await self.go.recv()
        return cast(str, raw_msg)

    async def send(self, msg: str):
        assert self.go

        await self.go.send(msg)

    def close(self):
        self.endpoint.close()


class ApiBackEnd(Backend):
    async def serve(self, host, port):
        await serve(self.bot.api_server_loop, host, port)
