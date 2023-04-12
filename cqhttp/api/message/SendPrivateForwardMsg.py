"""发送合并转发 ( 好友 )"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase
from cqhttp.api.message.SendGroupForwardMsg import ForwardNode


class Response(ResponseBase):
    class Data:
        message_id: int
        forward_id: str

    data: Data


@register_to_api
class SendPrivateForwardMsg(ApiAction[Response]):
    """发送合并转发 ( 好友 )"""

    action = "send_private_forward_msg"
    response: Response

    def __init__(
        self, user_id: int, messages: list[ForwardNode], *, echo: Optional[str] = None
    ):
        super().__init__()
        self.response = Response()
        self.user_id = user_id
        self.messages = messages
        self.echo = echo
