from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class QidianGetAccountInfo(ApiAction):
    """获取企点账号信息"""

    action = "qidian_get_account_info"

    def __init__(self, *, echo: Optional[str] = None):
        self.echo = echo
