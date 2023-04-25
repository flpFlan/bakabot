"""获取中文分词 ( 隐藏 API )"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        slices: list[str]

    data: Data


@register_to_api
class GetWordSlices(ApiAction[Response]):
    """获取中文分词 ( 隐藏 API )"""

    action = ".get_word_slices"
    response: Response

    def __init__(self, content: str, *, echo: Optional[str] = None):
        super().__init__()
        self.response = Response()
        self.content = content
        self.echo = echo
