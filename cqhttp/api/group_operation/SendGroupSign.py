"""群打卡"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


@register_to_api
class SendGroupSign(ApiAction[ResponseBase]):
    """群打卡"""

    action = "send_group_sign"

    def __init__(self, group_id: int, *, echo: Optional[str] = None):
        super().__init__()
        self.response = ResponseBase()
        self.message_id = group_id
        self.echo = echo
