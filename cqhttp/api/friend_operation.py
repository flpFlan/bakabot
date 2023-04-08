"""好友操作 API"""
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class DeleteFriend(ApiAction):
    action = "delete_friend"

    def __init__(self, user_id: int, *, echo: str = ""):
        self.user_id = user_id
        self.echo = echo


@register_to_api
class DeleteUnidirectionalFriend(ApiAction):
    action = "delete_unidirectional_friend"

    def __init__(self, user_id: int, *, echo: str = ""):
        self.user_id = user_id
        self.echo = echo
