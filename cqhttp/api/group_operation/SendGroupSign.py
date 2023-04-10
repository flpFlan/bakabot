"""群打卡"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class SendGroupSign(ApiAction):
    """群打卡"""

    action = "send_group_sign"

    def __init__(self, group_id: int, *, echo: Optional[str] = None):
        self.message_id = group_id
        self.echo = echo
