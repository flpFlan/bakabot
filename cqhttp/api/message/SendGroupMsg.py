"""发送群聊消息"""
import asyncio
import threading
import time
from typing import Optional

from click import echo
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        message_id: int

    data: Data


@register_to_api
class SendGroupMsg(ApiAction[Response]):
    """发送群聊消息"""

    action = "send_group_msg"
    response: Response

    def __init__(
        self,
        group_id: int,
        message: str,
        auto_escape: bool = False,
        *,
        echo: Optional[str] = None
    ):
        super().__init__()
        self.response = Response()
        self.group_id = group_id
        self.message = message
        self.auto_escape = auto_escape
        self.echo = echo

    @staticmethod
    def many(
        group_list: list[int] | set[int],
        message: str,
        auto_escape: bool = False,
        *,
        echo: Optional[str] = None
    ):
        return SendManyGroupMsg(group_list, message, auto_escape, echo=echo)


class SendManyGroupMsg:
    def __init__(
        self,
        group_list: list[int] | set[int],
        message: str,
        auto_escape: bool = False,
        *,
        echo: Optional[str] = None
    ):
        self.group_list = group_list
        self.message = message
        self.auto_escape = auto_escape
        self.echo = echo

    def do(self, bot, interval=3):
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
                ).do(bot)
                asyncio.run(task)
                time.sleep(interval)

        threading.Thread(name="send_groups_msg", target=target).start()
