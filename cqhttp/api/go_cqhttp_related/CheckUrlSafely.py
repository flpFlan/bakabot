"""检查链接安全性"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction,  ResponseBase

class Data(TypedDict):
    level: int
    
class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class CheckUrlSafely(ApiAction[Response]):
    """检查链接安全性"""

    action:str = field(init=False,default="check_url_safely")
    url: str
