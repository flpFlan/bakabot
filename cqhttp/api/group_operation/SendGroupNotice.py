"""发送群公告"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class SendGroupNotice(ApiAction):
    """发送群公告"""

    action = "_send_group_notice"

    def __init__(
        self,
        group_id: int,
        content: str,
        image: Optional[str] = None,
        *,
        echo: Optional[str] = None
    ):
        self.group_id = group_id
        self.content = content
        if image:
            self.image = image
        self.echo = echo
