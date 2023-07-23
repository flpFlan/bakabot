"""发送私聊消息"""
import asyncio
from dataclasses import dataclass, field
import inspect
from typing import Callable, Optional, TypedDict
from cqhttp.api.base import ApiAction, ResponseBase
from cqhttp.cqcode.base import CQCode
from cqhttp.api.friend_info.GetStrangerInfo import (
    GetStrangerInfo,
    Response as FriendInfoResponse,
)


class Data(TypedDict):
    message_id: int


class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class SendPrivateMsg(ApiAction[Response]):
    """发送私聊消息"""

    action: str = field(init=False, default="send_private_msg")
    user_id: int
    message: str | bool | CQCode
    group_id: Optional[int] = None
    auto_escape: bool = False

    @staticmethod
    def many(
        target_list: list[int] | set[int],
        message: str | CQCode | Callable[[FriendInfoResponse], str],
        auto_escape: bool = False,
        *,
        echo: Optional[str] = None
    ):
        return SendManyPrivateMsg(target_list, message, auto_escape, echo=echo)


class SendManyPrivateMsg:
    def __init__(
        self,
        group_list: list[int] | set[int],
        message: str | CQCode | Callable[[FriendInfoResponse], str],
        auto_escape: bool = False,
        *,
        echo: Optional[str] = None
    ):
        self.target_list = group_list
        self.message = message
        self.auto_escape = auto_escape
        self.echo = echo
        self._interval = 3

    def interval(self, interval: float):
        self._interval = interval
        return self

    def forget(self):
        async def target():
            target_list = self.target_list
            message = self.message
            auto_escape = self.auto_escape
            echo = self.echo
            interval = self._interval
            for qq_number in target_list:
                if inspect.isfunction(message):
                    r = await GetStrangerInfo(user_id=qq_number).do()
                    message = message(r)
                message = str(message)
                await SendPrivateMsg(
                    user_id=qq_number,
                    message=message,
                    auto_escape=auto_escape,
                    echo=echo,
                ).do()
                await asyncio.sleep(interval)

        _t = asyncio.create_task(target())
