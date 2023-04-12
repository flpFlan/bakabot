"""设置群管理员"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


@register_to_api
class SetGroupAdmin(ApiAction[ResponseBase]):
    """设置群管理员"""

    action = "set_group_admin"

    def __init__(
        self,
        group_id: int,
        user_id: int,
        enable: bool = True,
        *,
        echo: Optional[str] = None
    ):
        super().__init__()
        self.response = ResponseBase()
        self.group_id = group_id
        self.user_id = user_id
        self.enable = enable
        self.echo = echo
