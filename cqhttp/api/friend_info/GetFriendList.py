"""获取好友列表"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction,  ResponseBase

class Data(TypedDict):
    user_id: int
    nickname: str
    remark: str
    
class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetFriendList(ApiAction[Response]):
    """获取好友列表"""

    action:str = field(init=False,default="get_friend_list")
