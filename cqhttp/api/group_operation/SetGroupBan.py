"""群单人禁言"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


@register_to_api
class SetGroupBan(ApiAction[ResponseBase]):
    """群单人禁言"""

    action = "set_group_ban"

    def __init__(
        self,
        group_id: int,
        user_id: int,
        duration: int = 30 * 60,
        *,
        echo: Optional[str] = None
    ):
        super().__init__()
        self.response = ResponseBase()
        self.group_id = group_id
        self.user_id = user_id
        self.duration = duration
        self.echo = echo
