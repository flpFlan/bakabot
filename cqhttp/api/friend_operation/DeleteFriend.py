"""删除好友"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction, ResponseBase


@ApiAction.register
@dataclass
class DeleteFriend(ApiAction[ResponseBase]):
    """删除好友"""

    action:str = field(init=False,default="delete_friend")
    user_id: int
