"""发送合并转发 ( 群聊 )"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction,  ResponseBase

@dataclass
class ForwardNode:
    id: int
    name: str
    uin: int
    content: str
    seq: str

class Data(TypedDict):
    message_id: int
    forward_id: str

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class SendGroupForwardMsg(ApiAction[Response]):
    """发送合并转发 ( 群聊 )"""

    action:str = field(init=False,default="send_group_forward_msg")
    group_id: int
    messages: list[ForwardNode]
