"""获取 QQ 相关接口凭证"""
from dataclasses import dataclass, field
from typing import Optional, TypedDict
from cqhttp.api.base import ApiAction,  ResponseBase

class Data(TypedDict):
    cookies: str
    csrf_token: int

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetCredentials(ApiAction[Response]):
    """获取 QQ 相关接口凭证"""

    action:str = field(init=False,default="get_credentials")
    domain: Optional[str] = None
