"""设置群管理员"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction,  ResponseBase


@ApiAction.register
@dataclass
class SetGroupAdmin(ApiAction[ResponseBase]):
    """设置群管理员"""

    action:str = field(init=False,default="set_group_admin")
    group_id: int
    user_id: int
    enable: bool = True
