"""发送私聊消息"""
import asyncio
import threading
import time
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        message_id: int

    data: Data


@register_to_api
class SendPrivateMsg(ApiAction[Response]):
    """发送私聊消息"""

    action = "send_private_msg"
    response: Response

    def __init__(
        self,
        user_id: int,
        message: str,
        group_id: Optional[int] = None,
        auto_escape: bool = False,
        *,
        echo: Optional[str] = None
    ):
        super().__init__()
        self.response = Response()
        self.user_id = user_id
        self.group_id = group_id
        self.message = message
        self.auto_escape = auto_escape
        self.echo = echo

    @staticmethod
    def many(
        target_list: list[int] | set[int],
        message: str,
        auto_escape: bool = False,
        *,
        echo: Optional[str] = None
    ):
        return SendManyPrivateMsg(target_list, message, auto_escape, echo=echo)


class SendManyPrivateMsg:
    def __init__(
        self,
        group_list: list[int] | set[int],
        message: str,
        auto_escape: bool = False,
        *,
        echo: Optional[str] = None
    ):
        self.target_list = group_list
        self.message = message
        self.auto_escape = auto_escape
        self.echo = echo

    def do(self, bot, interval=3):
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
                ).do(bot)
                asyncio.run(task)
                time.sleep(interval)

        threading.Thread(name="send_privates_msg", target=target).start()
