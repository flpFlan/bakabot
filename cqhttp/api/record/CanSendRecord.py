"""检查是否可以发送语音"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction, ResponseBase

class Data(TypedDict):
    yes: bool

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class CanSendRecord(ApiAction[Response]):
    """检查是否可以发送语音"""

    action:str = field(init=False,default="can_send_record")
