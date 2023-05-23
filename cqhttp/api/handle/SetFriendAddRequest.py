"""处理加好友请求"""
from dataclasses import dataclass, field
from typing import Optional
from cqhttp.api.base import ApiAction,  ResponseBase


@ApiAction.register
@dataclass
class SetFriendAddRequest(ApiAction[ResponseBase]):
    """处理加好友请求"""

    action:str = field(init=False,default="set_friend_add_request")
    flag: str
    approve: bool = False
    remark: Optional[str]=None
