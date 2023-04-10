"""检查是否可以发送语音"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        yes: bool

    data: Data


@register_to_api
class CanSendRecord(ApiAction[Response]):
    """检查是否可以发送语音"""

    action = "can_send_record"
    response = Response()

    def __init__(self, *, echo: Optional[str] = None):
        self.echo = echo
