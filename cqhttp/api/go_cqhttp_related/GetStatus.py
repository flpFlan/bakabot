"""获取状态"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction, ResponseBase


class Statistics(TypedDict):
    PacketReceived: int
    PacketSent: int
    PacketLost: int
    MessageReceived: int
    MessageSent: int
    DisconnectTimes: int
    LostTimes: int
    LastMessageTime: int

class Data(TypedDict):
    app_initialized: bool
    app_enabled: bool
    plugins_good: bool
    app_good: bool
    online: bool
    good: bool
    stat: Statistics

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetStatus(ApiAction[Response]):
    """获取状态"""

    action:str = field(init=False,default="get_status")
