"""获取 CSRF Token"""
from dataclasses import dataclass, field
from typing import  TypedDict
from cqhttp.api.base import ApiAction, ResponseBase

class Data(TypedDict):
    token: int

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetCsrfToken(ApiAction[Response]):
    """获取 CSRF Token"""

    action:str = field(init=False,default="get_csrf_token")
