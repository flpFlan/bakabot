"""发送群聊消息"""
from typing import Optional
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
