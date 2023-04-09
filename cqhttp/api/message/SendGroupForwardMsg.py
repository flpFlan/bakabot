from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class ForwardNode:
    id: int
    name: str
    uin: int
    content: str
    seq: str


class Response(ResponseBase):
    class Data:
        message_id: int
        forward_id: str

    data: Data


@register_to_api
class SendGroupForwardMsg(ApiAction[Response]):
    """发送合并转发 ( 群聊 )"""

    action = "send_group_forward_msg"
    response = Response()

    def __init__(
        self, group_id: int, messages: list[ForwardNode], *, echo: Optional[str] = None
    ):
        self.group_id = group_id
        self.messages = messages
        self.echo = echo
