from cqhttp.events.base import CQHTTPEvent
from dataclasses import dataclass,field

@dataclass
class Request(CQHTTPEvent):
    post_type :str = "request"

    request_type: str = field(kw_only=True)


@CQHTTPEvent.register
@dataclass
class FriendRequest(Request):
    """加好友请求"""

    request_type :str = "friend"

    user_id: int = field(kw_only=True)
    comment: str = field(kw_only=True)
    flag: str = field(kw_only=True)

@dataclass
class GroupRequest(Request):
    """加群请求／邀请"""

    request_type :str = "group"

    sub_type: str = field(kw_only=True)
    group_id: int = field(kw_only=True)
    user_id: int = field(kw_only=True)
    comment: str = field(kw_only=True)
    flag: str = field(kw_only=True)


@CQHTTPEvent.register
@dataclass
class GroupAddRequest(GroupRequest):
    """加群请求"""

    sub_type:str = "add"


@CQHTTPEvent.register
@dataclass
class GroupInviteRequest(GroupRequest):
    """邀请登录号入群"""

    sub_type:str = "invite"