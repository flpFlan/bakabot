"""设置群名片 ( 群备注 )"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction, ResponseBase


@ApiAction.register
@dataclass
class SetGroupCard(ApiAction[ResponseBase]):
    """设置群名片 ( 群备注 )"""

    action:str = field(init=False,default="set_group_card")
    group_id: int
    user_id: int
    card: str = ""
