"""下载文件到缓存目录"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction,  ResponseBase

class Data(TypedDict):
    file: str
    
class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class DownloadFile(ApiAction[Response]):
    """下载文件到缓存目录"""

    action:str = field(init=False,default="download_file")
    url: str
    thread_count: int
    headers: str | list[str]
