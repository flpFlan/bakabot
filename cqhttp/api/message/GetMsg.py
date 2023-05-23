"""获取消息"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction, ResponseBase


class Sender(TypedDict):
    nickname: str
    user_id: int

class Data(TypedDict):
    group: bool
    message_id: int
    real_id: int
    message_type: str
    sender: Sender
    time: int
    message: str
    raw_message: str
    group_id: int | None

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetMsg(ApiAction[Response]):
    """获取消息"""

    action:str = field(init=False,default="get_msg")
    message_id: int
