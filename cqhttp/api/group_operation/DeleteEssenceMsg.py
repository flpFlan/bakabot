from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class DeleteEssenceMsg(ApiAction):
    """移出精华消息"""

    action = "delete_essence_msg"

    def __init__(self, message_id: int, *, echo: Optional[str] = None):
        self.message_id = message_id
        self.echo = echo
