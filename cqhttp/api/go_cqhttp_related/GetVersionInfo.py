"""获取版本信息"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction,  ResponseBase

class Data(TypedDict):
    app_name: str
    app_version: str
    app_full_name: str
    protocol_version: str
    coolq_edition: str
    coolq_directory: str
    plugin_version: str
    plugin_build_number: int
    plugin_build_configuration: str
    runtime_version: str
    runtime_os: str
    version: str
    protocol: str
    go_cqhttp: bool  # 响应字段为go-cqhttp，但是固定值true

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class GetVersionInfo(ApiAction[Response]):
    """获取版本信息"""

    action:str = field(init=False,default="get_version_info")
