"""获取 Cookies"""
from dataclasses import dataclass, field
from typing import Optional, TypedDict
from cqhttp.api.base import ApiAction,  ResponseBase

class Data(TypedDict):
    cookies: str

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetCookies(ApiAction[Response]):
    """获取 Cookies"""

    action:str = field(init=False,default="get_cookies")
    domain: Optional[str] = None