"""清理缓存"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction,  ResponseBase


@ApiAction.register
@dataclass
class CleanCache(ApiAction[ResponseBase]):
    """清理缓存"""

    action:str = field(init=False,default="clean_cache")
