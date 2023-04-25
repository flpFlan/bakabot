"""检查是否可以发送图片"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        yes: bool

    data: Data


@register_to_api
class CanSendImage(ApiAction[Response]):
    """检查是否可以发送图片"""

    action = "can_send_image"
    response: Response

    def __init__(self, *, echo: Optional[str] = None):
        super().__init__()
        self.response = Response()
        self.echo = echo
