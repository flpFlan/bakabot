"""群匿名用户禁言"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase
from cqhttp.events.message import GroupMessage


@register_to_api
class SetGroupAnonymousBan(ApiAction[ResponseBase]):
    """群匿名用户禁言"""

    action = "set_group_anonymous_ban"

    def __init__(
        self,
        group_id: int,
        *,
        anonymous: GroupMessage.Anonymous | None = None,
        anonymous_flag: str = "",
        duration: int = 30 * 60,
        echo: Optional[str] = None
    ):
        super().__init__()
        self.response = ResponseBase()
        self.group_id = group_id
        assert anonymous or anonymous_flag, "anonymous和anonymous_flag必须传入一个"
        if anonymous:
            self.anonymous = anonymous
        if anonymous_flag:
            self.anonymous_flag = anonymous_flag
        self.duration = duration
        self.echo = echo
