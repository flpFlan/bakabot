"""群打卡"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction,  ResponseBase


@ApiAction.register
@dataclass
class SendGroupSign(ApiAction[ResponseBase]):
    """群打卡"""

    action:str = field(init=False,default="send_group_sign")
    group_id: int