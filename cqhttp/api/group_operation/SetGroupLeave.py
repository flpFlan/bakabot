"""退出群组"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class SetGroupLeave(ApiAction):
    """退出群组"""

    action = "set_group_leave"

    def __init__(
        self, group_id: int, is_dismiss: bool = False, *, echo: Optional[str] = None
    ):
        self.group_id = group_id
        self.is_dismiss = is_dismiss
        self.echo = echo
