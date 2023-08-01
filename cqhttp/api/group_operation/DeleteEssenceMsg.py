"""移出精华消息"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction, ResponseBase


@ApiAction.register
@dataclass
class DeleteEssenceMsg(ApiAction[ResponseBase]):
    """移出精华消息"""

    action:str = field(init=False,default="delete_essence_msg")
    message_id: int
