"""获取语音"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        file: str

    data: Data


@register_to_api
class GetRecord(ApiAction[Response]):
    """获取语音"""

    action = "get_record"
    response: Response

    def __init__(self, file: str, out_format: str, *, echo: Optional[str] = None):
        super().__init__()
        self.response = Response()
        self.file = file
        self.out_format = out_format
        self.echo = echo
