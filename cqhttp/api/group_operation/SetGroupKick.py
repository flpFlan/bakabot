"""群组踢人"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


@register_to_api
class SetGroupKick(ApiAction[ResponseBase]):
    """群组踢人"""

    action = "set_group_kick"

    def __init__(
        self,
        group_id: int,
        user_id: int,
        reject_add_request: bool = False,
        *,
        echo: Optional[str] = None
    ):
        super().__init__()
        self.response = ResponseBase()
        self.group_id = group_id
        self.user_id = user_id
        self.reject_add_request = reject_add_request
        self.echo = echo
