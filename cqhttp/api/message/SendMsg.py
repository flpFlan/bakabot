"""发送消息"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        message_id: int

    data: Data


@register_to_api
class SendMsg(ApiAction[Response]):
    """发送消息"""

    action = "send_msg"
    response = Response()

    def __init__(
        self,
        message_type: Optional[str] = None,
        user_id: Optional[int] = None,
        group_id: Optional[int] = None,
        *,
        message: str,
        auto_escape: bool = False,
        echo: Optional[str] = None
    ):
        self.message_type = message_type
        self.user_id = user_id
        self.group_id = group_id
        self.message = message
        self.auto_escape = auto_escape
        self.echo = echo
