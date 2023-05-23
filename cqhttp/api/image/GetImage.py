"""获取图片信息"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction,  ResponseBase

class Data(TypedDict):
    size: int
    filename: str
    url: str

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetImage(ApiAction[Response]):
    """获取图片信息"""

    action:str = field(init=False,default="get_image")
    file: str
