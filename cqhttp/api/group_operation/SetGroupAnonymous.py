"""群设置匿名"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction, ResponseBase


@ApiAction.register
@dataclass
class SetGroupAnonymous(ApiAction[ResponseBase]):
    """群设置匿名"""

    action:str = field(init=False,default="set_group_anonymous")
    group_id: int
    enable: bool = True
