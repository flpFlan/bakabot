"""删除好友"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class DeleteFriend(ApiAction):
    """删除好友"""

    action = "delete_friend"

    def __init__(self, user_id: int, *, echo: Optional[str] = None):
        self.user_id = user_id
        self.echo = echo
