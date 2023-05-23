"""获取单向好友列表"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction,  ResponseBase

class Data(TypedDict):
    user_id: int
    nickname: str
    source: str
    
class Response(ResponseBase):
    data:Data
    


@ApiAction.register
@dataclass
class GetUnidirectionalFriendList(ApiAction[Response]):
    """获取单向好友列表"""

    action:str = field(init=False,default="get_unidirectional_friend_list")
