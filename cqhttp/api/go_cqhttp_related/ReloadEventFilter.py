"""重载事件过滤器"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction,  ResponseBase


@ApiAction.register
@dataclass
class ReloadEventFilter(ApiAction[ResponseBase]):
    """重载事件过滤器"""

    action:str = field(init=False,default="reload_event_filter")
    file: str
