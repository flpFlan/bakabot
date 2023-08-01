"""获取群公告"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction, ResponseBase

class Message(TypedDict):
    text: str
    images: list[str]
    
class NoticeInfo(TypedDict):
    sender_id: int
    publish_time: int
    message: Message

class Response(ResponseBase):
    data: list[NoticeInfo]


@ApiAction.register
@dataclass
class GetGroupNotice(ApiAction[Response]):
    """获取群公告"""

    action:str = field(init=False,default="_get_group_notice")
    group_id: int
