"""发送群聊消息"""
import asyncio
from dataclasses import dataclass, field
import inspect
from typing import Callable, Optional, TypedDict
from cqhttp.api.base import ApiAction, ResponseBase
from cqhttp.cqcode.base import CQCode
from cqhttp.api.group_info.GetGroupInfo import (
    GetGroupInfo,
    Response as GroupInfoResponse,
)


class Data(TypedDict):
    message_id: int


class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class SendGroupMsg(ApiAction[Response]):
    """发送群聊消息"""

    action: str = field(init=False, default="send_group_msg")
    group_id: int
    message: str | bool | CQCode
    auto_escape: bool = False

    @staticmethod
    def many(
        group_list: list[int] | set[int],
        message: str | CQCode | Callable[[GroupInfoResponse], str],
        auto_escape: bool = False,
        *,
        echo: Optional[str] = None
    ):
        return SendManyGroupMsg(group_list, message, auto_escape, echo=echo)


class SendManyGroupMsg:
    def __init__(
        self,
        group_list: list[int] | set[int],
        message: str | CQCode | Callable[[GroupInfoResponse], str],
        auto_escape: bool = False,
        *,
        echo: Optional[str] = None
    ):
        self.group_list = group_list
        self.message = message
        self.auto_escape = auto_escape
        self.echo = echo
        self._interval = 3.

    def interval(self, interval: float):
        self._interval = interval
        return self

    def forget(self):
        async def target():
            group_list = self.group_list
            message = self.message
            auto_escape = self.auto_escape
            echo = self.echo
            interval = self._interval
            for group_id in group_list:
                if inspect.isfunction(message):
                    r = await GetGroupInfo(group_id=group_id).do()
                    message = message(r)
                message = str(message)
                await SendGroupMsg(
                    group_id=group_id,
                    message=message,
                    auto_escape=auto_escape,
                    echo=echo,
                ).do()
                await asyncio.sleep(interval)

        _t = asyncio.create_task(target())
