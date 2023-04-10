"""设置群名片 ( 群备注 )"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class SetGroupCard(ApiAction):
    """设置群名片 ( 群备注 )"""

    action = "set_group_card"

    def __init__(
        self, group_id: int, user_id: int, card: str = "", *, echo: Optional[str] = None
    ):
        self.group_id = group_id
        self.user_id = user_id
        self.card = card
        self.echo = echo
