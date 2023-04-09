from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class SetGroupName(ApiAction):
    """设置群名"""

    action = "set_group_name"

    def __init__(self, group_id: int, group_name: str, *, echo: Optional[str] = None):
        self.group_id = group_id
        self.group_name = group_name
        self.echo = echo
