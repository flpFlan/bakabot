"""获取合并转发内容"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        class ForwardMessage:
            class Sender:
                nickname: str
                user_id: int

            content: str
            sender: Sender
            time: int

        messages: list

    data: Data


@register_to_api
class GetForwardMsg(ApiAction[Response]):
    """获取合并转发内容"""

    action = "get_forward_msg"
    response: Response

    def __init__(self, message_id: int, *, echo: Optional[str] = None):
        super().__init__()
        self.response = Response()
        self.message_id = message_id
        self.echo = echo
