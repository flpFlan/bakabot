"""设置在线机型"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class SetModelShow(ApiAction):
    """设置在线机型"""

    action = "_set_model_show"

    def __init__(self, model: str, model_show: str, *, echo: Optional[str] = None):
        self.model = model
        self.model_show = model_show
        self.echo = echo
