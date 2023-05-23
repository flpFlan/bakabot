"""设置精华消息"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction, ResponseBase


@ApiAction.register
@dataclass
class SetEssenceMsg(ApiAction[ResponseBase]):
    """设置精华消息"""

    action:str = field(init=False,default="set_essence_msg")
    message_id: int