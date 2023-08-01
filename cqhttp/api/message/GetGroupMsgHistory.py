"""获取群消息历史记录"""
from dataclasses import dataclass, field
from typing import Optional, TypedDict
from cqhttp.api.base import ApiAction, ResponseBase
from cqhttp.events.message import GroupMessage

class Data(TypedDict):
    messages: list[GroupMessage]

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetGroupMsgHistory(ApiAction[Response]):
    """获取群消息历史记录"""

    action:str = field(init=False,default="get_group_msg_history")
    group_id: int
    message_seq: Optional[int] = None
