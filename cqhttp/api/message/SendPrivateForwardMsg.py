"""发送合并转发 ( 好友 )"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction, ResponseBase
from cqhttp.api.message.SendGroupForwardMsg import ForwardNode

class Data(TypedDict):
    message_id: int
    forward_id: str

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class SendPrivateForwardMsg(ApiAction[Response]):
    """发送合并转发 ( 好友 )"""

    action:str = field(init=False,default="send_private_forward_msg")
    user_id: int
    messages: list[ForwardNode]
