from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class SetGroupSpecialTitle(ApiAction):
    """设置群组专属头衔"""

    action = "set_group_special_title"

    def __init__(
        self,
        group_id: int,
        user_id: int,
        special_title: str = "",
        duration: int = -1,
        *,
        echo: Optional[str] = None
    ):
        self.group_id = group_id
        self.user_id = user_id
        self.special_title = special_title
        self.duration = duration
        self.echo = echo
