"""发送私聊消息"""
import asyncio
from dataclasses import dataclass, field
import threading
import time
from typing import Optional, TypedDict
from cqhttp.api.base import ApiAction, ResponseBase
from cqhttp.cqcode.base import CQCode


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
        message: str | CQCode,
        auto_escape: bool = False,
        *,
        echo: Optional[str] = None
    ):
        return SendManyPrivateMsg(target_list, str(message), auto_escape, echo=echo)


class SendManyPrivateMsg:
    def __init__(
        self,
        group_list: list[int] | set[int],
        message: str | CQCode,
        auto_escape: bool = False,
        *,
        echo: Optional[str] = None
    ):
        self.target_list = group_list
        self.message = message
        self.auto_escape = auto_escape
        self.echo = echo

    def forget(self, interval=3):
        def target():
            target_list = self.target_list
            message = self.message
            auto_escape = self.auto_escape
            echo = self.echo
            for qq_number in target_list:
                task = SendPrivateMsg(
                    user_id=qq_number,
                    message=message,
                    auto_escape=auto_escape,
                    echo=echo,
                ).do()
                asyncio.run(task)
                time.sleep(interval)

        threading.Thread(name="send_privates_msg", target=target).start()
