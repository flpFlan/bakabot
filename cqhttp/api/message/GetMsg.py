"""获取消息"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        class Sender:
            nickname: str
            user_id: int

        group: bool
        group_id: int | None = None
        message_id: int
        real_id: int
        message_type: str
        sender: Sender
        time: int
        message: str
        raw_message: str

    data: Data


@register_to_api
class GetMsg(ApiAction[Response]):
    """获取消息"""

    action = "get_msg"
    response = Response()

    def __init__(self, message_id: int, *, echo: Optional[str] = None):
        self.message_id = message_id
        self.echo = echo
