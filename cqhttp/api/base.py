# -- stdlib --
from asyncio import Future
from typing import Type, Optional, cast, TypeVar, Generic

# -- third party --
# -- own --
from cqhttp.base import Event, EventArgs

# -- code --


class ApiActionArgs(EventArgs):
    def __init__(self):
        super().__init__()
        self.args = {}


class ResponseBase:
    status: str
    retcode: int
    msg: str | None = None
    wording: str | None = None
    data: object
    echo: Optional[str]


TResponse = TypeVar("TResponse", bound=ResponseBase)


class ApiAction(Event, Generic[TResponse]):
    action: str
    echo: Optional[str]
    response: Optional[TResponse]

    def __init__(self):
        self._ = ApiActionArgs()

    def bind(self, bot):
        from bot import Bot

        class Bind:
            def __init__(self, act, bot):
                self.act = cast(ApiAction, act)
                self.bot = cast(Bot, bot)

            async def do(self) -> TResponse | None:
                bot = self.bot
                act = self.act
                await bot.behavior.post_api(act)
                return act.response

        from bot import Bot

        self.bot = bot = cast(Bot, bot)
        return Bind(self, bot)

    async def do(self, bot=None) -> TResponse | None:
        if bot:
            self.bot = bot
        assert self.bot
        await self.bot.behavior.post_api(self)
        return self.response

    def _callback(self):
        ...


all_apis = []


def register_to_api(act):
    all_apis.append(act)
    return act
