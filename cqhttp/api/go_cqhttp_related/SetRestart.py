"""重启 Go-CqHttp"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction,  ResponseBase


@ApiAction.register
@dataclass
class SetRestart(ApiAction[ResponseBase]):
    """重启 Go-CqHttp"""

    action:str = field(init=False,default="set_restart")
    delay: int = 0
