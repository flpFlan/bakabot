"""移出精华消息"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


@register_to_api
class DeleteEssenceMsg(ApiAction[ResponseBase]):
    """移出精华消息"""

    action = "delete_essence_msg"

    def __init__(self, message_id: int, *, echo: Optional[str] = None):
        super().__init__()
        self.response = ResponseBase()
        self.message_id = message_id
        self.echo = echo
