from cqhttp.events.base import CQHTTPEvent
from cqhttp.events.base import register_to_events


class Request(CQHTTPEvent):
    post_type = "request"
    request_type: str


@register_to_events
class FriendRequest(Request):
    """加好友请求"""

    request_type = "friend"

    user_id: int
    comment: str
    flag: str


class GroupRequest(Request):
    """加群请求／邀请"""

    request_type = "group"

    sub_type: str
    group_id: int
    user_id: int
    comment: str
    flag: str


@register_to_events
class GroupAddRequest(GroupRequest):
    """加群请求"""

    sub_type = "add"


@register_to_events
class GroupInviteRequest(GroupRequest):
    """邀请登录号入群"""

    sub_type = "invite"
