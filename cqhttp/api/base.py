# -- stdlib --
from typing import Type, Optional, cast, TypeVar, Generic

# -- third party --
# -- own --


# -- code --


class ResponseBase:
    status: str
    retcode: int
    msg: str | None = None
    wording: str | None = None
    data: object
    echo: Optional[str]


TResponse = TypeVar("TResponse", bound=ResponseBase)


class ApiAction(Generic[TResponse]):
    action: str
    echo: Optional[str]
    response: Optional[TResponse]

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


all_apis = []


def register_to_api(act):
    all_apis.append(act)
    return act
