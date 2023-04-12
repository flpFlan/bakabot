"""下载文件到缓存目录"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        file: str

    data: Data


@register_to_api
class DownloadFile(ApiAction[Response]):
    """下载文件到缓存目录"""

    action = "download_file"
    response: Response

    def __init__(
        self,
        url: str,
        thread_count: int,
        headers: str | list[str],
        *,
        echo: Optional[str] = None
    ):
        super().__init__()
        self.response = Response()
        self.url = url
        self.thread_count = thread_count
        self.headers = headers
        self.echo = echo
