"""删除单向好友"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction,  ResponseBase


@ApiAction.register
@dataclass
class DeleteUnidirectionalFriend(ApiAction[ResponseBase]):
    """删除单向好友"""

    action:str = field(init=False,default="delete_unidirectional_friend")
    user_id: int
