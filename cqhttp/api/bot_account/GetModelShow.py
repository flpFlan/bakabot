from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        variants: list

    data: Data


@register_to_api
class GetModelShow(ApiAction[Response]):
    """获取在线机型"""

    action = "_get_model_show"
    response = Response()

    def __init__(self, model: str, *, echo: Optional[str] = None):
        self.model = model
        self.echo = echo
