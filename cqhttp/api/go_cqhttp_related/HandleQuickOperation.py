from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class HandleQuickOperation(ApiAction):
    """对事件执行快速操作 ( 隐藏 API )"""

    action = ".handle_quick_operation"

    def __init__(
        self, context: object, operation: object, *, echo: Optional[str] = None
    ):
        self.context = context
        self.operation = operation
        self.echo = echo
