"""获取语音"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction, ResponseBase

class Data(TypedDict):
    file: str

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetRecord(ApiAction[Response]):
    """获取语音"""

    action:str = field(init=False,default="get_record")
    file: str
    out_format: str
