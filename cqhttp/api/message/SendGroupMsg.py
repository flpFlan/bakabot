"""发送群聊消息"""
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
class SendGroupMsg(ApiAction[Response]):
    """发送群聊消息"""

    action: str = field(init=False, default="send_group_msg")
    group_id: int
    message: str | bool | CQCode
    auto_escape: bool = False

    @staticmethod
    def many(
        group_list: list[int] | set[int],
        message: str | CQCode,
        auto_escape: bool = False,
        *,
        echo: Optional[str] = None
    ):
        return SendManyGroupMsg(group_list, str(message), auto_escape, echo=echo)


class SendManyGroupMsg:
    def __init__(
        self,
        group_list: list[int] | set[int],
        message: str | CQCode,
        auto_escape: bool = False,
        *,
        echo: Optional[str] = None
    ):
        self.group_list = group_list
        self.message = message
        self.auto_escape = auto_escape
        self.echo = echo

    def forget(self, interval=3):
        def target():
            group_list = self.group_list
            message = self.message
            auto_escape = self.auto_escape
            echo = self.echo
            for group_id in group_list:
                task = SendGroupMsg(
                    group_id=group_id,
                    message=message,
                    auto_escape=auto_escape,
                    echo=echo,
                ).do()
                asyncio.run(task)
                time.sleep(interval)

        threading.Thread(name="send_groups_msg", target=target).start()
