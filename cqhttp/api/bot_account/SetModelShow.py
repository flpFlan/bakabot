"""设置在线机型"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction,  ResponseBase


@ApiAction.register
@dataclass
class SetModelShow(ApiAction[ResponseBase]):
    """设置在线机型"""

    action:str = field(init=False,default="_set_model_show")
    model: str
    model_show: str