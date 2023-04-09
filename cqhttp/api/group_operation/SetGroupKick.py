from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class SetGroupKick(ApiAction):
    """群组踢人"""

    action = "set_group_kick"

    def __init__(
        self,
        group_id: int,
        user_id: int,
        reject_add_request: bool = False,
        *,
        echo: Optional[str] = None
    ):
        self.group_id = group_id
        self.user_id = user_id
        self.reject_add_request = reject_add_request
        self.echo = echo
