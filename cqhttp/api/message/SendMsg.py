"""发送消息"""
from dataclasses import dataclass, field
from typing import Optional, TypedDict
from cqhttp.api.base import ApiAction,  ResponseBase
from cqhttp.cqcode.base import CQCode

class Data(TypedDict):
    message_id: int

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class SendMsg(ApiAction[Response]):
    """发送消息"""

    action:str = field(init=False,default="send_msg")
    message: str | CQCode
    message_type: Optional[str] = None
    user_id: Optional[int] = None
    group_id: Optional[int] = None
    auto_escape: bool = False
