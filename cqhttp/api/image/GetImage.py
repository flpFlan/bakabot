from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        size: int
        filename: str
        url: str

    data: Data


@register_to_api
class GetImage(ApiAction[Response]):
    """获取图片信息"""

    action = "get_image"
    response = Response()

    def __init__(self, file: str, *, echo: Optional[str] = None):
        self.file = file
        self.echo = echo
