"""有关 Bot 账号的相关 API"""

from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class GetLoginInfo(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            user_id: int
            nickname: str

        data: Data

    action = "get_login_info"

    def __init__(self, echo: str = ""):
        self.echo = echo


@register_to_api
class SetQQProfile(ApiAction):
    action = "set_qq_profile"

    def __init__(
        self,
        nickname: str,
        company: str,
        email: str,
        college: str,
        personal_note: str,
        *,
        echo: str = ""
    ):
        self.nickname = nickname
        self.company = company
        self.email = email
        self.college = college
        self.personal_note = personal_note
        self.echo = echo


@register_to_api
class QidianGetAccountInfo(ApiAction):
    action = "qidian_get_account_info"

    def __init__(self, *, echo: str = ""):
        self.echo = echo


@register_to_api
class GetModelShow(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            variants: list

        data: Data

    action = "_get_model_show"

    def __init__(self, model: str, *, echo: str = ""):
        self.model = model
        self.echo = echo


@register_to_api
class SetModelShow(ApiAction):
    action = "_set_model_show"

    def __init__(self, model: str, model_show: str, *, echo: str = ""):
        self.model = model
        self.model_show = model_show
        self.echo = echo


@register_to_api
class GetOnlineClients(ApiAction):
    class Response(ApiAction.Response):
        clients: list

    action = "get_online_clients"

    def __init__(self, no_cache: bool, *, echo: str = ""):
        self.no_cache = no_cache
        self.echo = echo
