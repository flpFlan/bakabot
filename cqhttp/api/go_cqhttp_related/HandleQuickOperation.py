"""对事件执行快速操作 ( 隐藏 API )"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


@register_to_api
class HandleQuickOperation(ApiAction[ResponseBase]):
    """对事件执行快速操作 ( 隐藏 API )"""

    action = ".handle_quick_operation"

    def __init__(
        self, context: object, operation: object, *, echo: Optional[str] = None
    ):
        super().__init__()
        self.response = ResponseBase()
        self.context = context
        self.operation = operation
        self.echo = echo
