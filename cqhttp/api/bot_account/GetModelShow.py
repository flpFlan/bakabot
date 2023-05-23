"""获取在线机型"""
from dataclasses import dataclass, field
from typing import Optional, TypedDict
from cqhttp.api.base import ApiAction, ResponseBase

class Data(TypedDict):
    variants: list

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetModelShow(ApiAction[Response]):
    """获取在线机型"""

    action:str = field(init=False,default="_get_model_show")
    model: str
