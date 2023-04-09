from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class SetFriendAddRequest(ApiAction):
    """处理加好友请求"""

    action = "set_friend_add_request"

    def __init__(
        self,
        flag: str,
        approve: bool = False,
        remark: str = "",
        *,
        echo: Optional[str] = None
    ):
        self.flag = flag
        self.approve = approve
        self.remark = remark
        self.echo = echo
