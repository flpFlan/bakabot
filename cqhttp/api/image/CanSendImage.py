"""检查是否可以发送图片"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction, ResponseBase

class Data(TypedDict):
    yes: bool

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class CanSendImage(ApiAction[Response]):
    """检查是否可以发送图片"""

    action:str = field(init=False,default="can_send_image")
