"""对事件执行快速操作 ( 隐藏 API )"""
from dataclasses import dataclass, field
from cqhttp.api.base import ApiAction, ResponseBase


@ApiAction.register
@dataclass
class HandleQuickOperation(ApiAction[ResponseBase]):
    """对事件执行快速操作 ( 隐藏 API )"""

    action:str = field(init=False,default=".handle_quick_operation")
    context: object
    operation: object
