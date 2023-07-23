from cqhttp.events.base import CQHTTPEvent


class Request(CQHTTPEvent):
    post_type: str = "request"

    request_type: str


@CQHTTPEvent.register
class FriendRequest(Request):
    """加好友请求"""

    request_type: str = "friend"

    user_id: int
    comment: str
    flag: str


class GroupRequest(Request):
    """加群请求／邀请"""

    request_type: str = "group"

    sub_type: str
    group_id: int
    user_id: int
    comment: str
    flag: str


@CQHTTPEvent.register
class GroupAddRequest(GroupRequest):
    """加群请求"""

    sub_type: str = "add"


@CQHTTPEvent.register
class GroupInviteRequest(GroupRequest):
    """邀请登录号入群"""

    sub_type: str = "invite"
