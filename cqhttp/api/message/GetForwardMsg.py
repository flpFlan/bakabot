"""获取合并转发内容"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction,ResponseBase


class Sender(TypedDict):
    nickname: str
    user_id: int

class ForwardMessage(TypedDict):
    content: str
    sender: Sender
    time: int

class Data(TypedDict):
    messages: list[ForwardMessage]

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetForwardMsg(ApiAction[Response]):
    """获取合并转发内容"""

    action:str = field(init=False,default="get_forward_msg")
    message_id: int
