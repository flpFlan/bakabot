"""撤回消息"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction, ResponseBase


@ApiAction.register
@dataclass
class DeleteMsg(ApiAction[ResponseBase]):
    """撤回消息"""

    action:str = field(init=False,default="delete_msg")
    message_id: int
