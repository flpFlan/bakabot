"""获取状态"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        class Statistics:
            PacketReceived: int
            PacketSent: int
            PacketLost: int
            MessageReceived: int
            MessageSent: int
            DisconnectTimes: int
            LostTimes: int
            LastMessageTime: int

        app_initialized: bool
        app_enabled: bool
        plugins_good: bool
        app_good: bool
        online: bool
        good: bool
        stat: Statistics

    data: Data


@register_to_api
class GetStatus(ApiAction[Response]):
    """获取状态"""

    action = "get_status"
    response = Response()

    def __init__(self, *, echo: Optional[str] = None):
        self.echo = echo
