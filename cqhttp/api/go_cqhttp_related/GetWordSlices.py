"""获取中文分词 ( 隐藏 API )"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction, ResponseBase

class Data(TypedDict):
    slices: list[str]

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetWordSlices(ApiAction[Response]):
    """获取中文分词 ( 隐藏 API )"""

    action:str = field(init=False,default=".get_word_slices")
    content: str
