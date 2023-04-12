"""群全员禁言"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


@register_to_api
class SetGroupWholeBan(ApiAction[ResponseBase]):
    """群全员禁言"""

    action = "set_group_whole_ban"

    def __init__(
        self, group_id: int, enable: bool = True, *, echo: Optional[str] = None
    ):
        super().__init__()
        self.response = ResponseBase()
        self.group_id = group_id
        self.enable = enable
        self.echo = echo
