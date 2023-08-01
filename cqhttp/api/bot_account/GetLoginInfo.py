"""获取登录号信息"""
from typing import TypedDict
from cqhttp.api.base import ApiAction, ResponseBase
from dataclasses import dataclass,field

class Data(TypedDict):
    user_id: int
    nickname: str
        
class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetLoginInfo(ApiAction[Response]):
    """获取登录号信息"""

    action:str = field(init=False,default="get_login_info")
