"""删除单向好友"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


@register_to_api
class DeleteUnidirectionalFriend(ApiAction[ResponseBase]):
    """删除单向好友"""

    action = "delete_unidirectional_friend"

    def __init__(self, user_id: int, *, echo: Optional[str] = None):
        super().__init__()
        self.response = ResponseBase()
        self.user_id = user_id
        self.echo = echo
