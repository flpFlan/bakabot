"""发送私聊消息"""
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
