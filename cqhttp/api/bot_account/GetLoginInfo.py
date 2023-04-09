from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        user_id: int
        nickname: str

    data: Data


@register_to_api
class GetLoginInfo(ApiAction[Response]):
    """获取登录号信息"""

    action = "get_login_info"
    response = Response()

    def __init__(self, *, echo: str = ""):
        self.echo = echo
