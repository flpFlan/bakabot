"""标记消息已读"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction,  ResponseBase


@ApiAction.register
@dataclass
class MarkMsgAsRead(ApiAction[ResponseBase]):
    """标记消息已读"""

    action:str = field(init=False,default="mark_msg_as_read")
    message_id: int
