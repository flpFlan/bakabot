"""获取版本信息"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        app_name: str
        app_version: str
        app_full_name: str
        protocol_version: str
        coolq_edition: str
        coolq_directory: str
        go_cqhttp: bool = True  # 响应字段为go-cqhttp，但是固定值true
        plugin_version: str
        plugin_build_number: int
        plugin_build_configuration: str
        runtime_version: str
        runtime_os: str
        version: str
        protocol: str

    data: Data


@register_to_api
class GetVersionInfo(ApiAction[Response]):
    """获取版本信息"""

    action = "get_version_info"
    response = Response()

    def __init__(self, *, echo: Optional[str] = None):
        self.echo = echo
