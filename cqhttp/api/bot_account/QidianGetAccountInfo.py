"""获取企点账号信息"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction,  ResponseBase


@ApiAction.register
@dataclass
class QidianGetAccountInfo(ApiAction[ResponseBase]):
    """获取企点账号信息"""

    action:str = field(init=False,default="qidian_get_account_info")