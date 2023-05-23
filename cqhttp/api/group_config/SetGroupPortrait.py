"""设置群头像"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction, ResponseBase


@ApiAction.register
@dataclass
class SetGroupPortrait(ApiAction[ResponseBase]):
    """设置群头像"""

    action:str = field(init=False,default="set_group_portrait")
    group_id: int
    file: str
    cache: int = 1
