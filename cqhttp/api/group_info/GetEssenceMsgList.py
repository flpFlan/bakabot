"""获取精华消息列表"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction,  ResponseBase

class Element(TypedDict):
    sender_id: int
    sender_nick: str
    sender_time: int
    operator_id: int
    operator_nick: str
    operator_time: int
    message_id: int

class Response(ResponseBase):
    data: list[Element]


@ApiAction.register
@dataclass
class GetEssenceMsgList(ApiAction[Response]):
    """获取精华消息列表"""

    action:str = field(init=False,default="get_essence_msg_list")
    group_id: int
