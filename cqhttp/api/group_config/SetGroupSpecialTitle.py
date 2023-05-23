"""设置群组专属头衔"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction, ResponseBase


@ApiAction.register
@dataclass
class SetGroupSpecialTitle(ApiAction[ResponseBase]):
    """设置群组专属头衔"""

    action:str = field(init=False,default="set_group_special_title")
    group_id: int
    user_id: int
    special_title: str = ""
    duration: int = -1
