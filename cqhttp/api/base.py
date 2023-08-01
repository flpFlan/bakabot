# -- stdlib --
import asyncio
from typing import Optional, TypeVar, Generic, TypedDict
from dataclasses import dataclass, field

# -- third party --
# -- own --
from cqhttp.base import Event
from accio import ACCIO

# -- code --


class ResponseBase(TypedDict):
    status: str
    retcode: int
    msg: Optional[str]
    wording: Optional[str]
    echo: Optional[str]


TResponse = TypeVar("TResponse", bound=ResponseBase)


@dataclass
class ApiAction(Event, Generic[TResponse]):
    classes = set()

    action: str = field(kw_only=True)
    echo: Optional[str] = field(default=None, kw_only=True)

    async def do(self) -> TResponse:
        return await ACCIO.bot.behavior.post_api(self)

    def forget(self):
        _t = asyncio.create_task(ACCIO.bot.behavior.post_api(self))

    @staticmethod
    def register(act):
        ApiAction.classes.add(act)
        Event.classes.add(act)
        return act
