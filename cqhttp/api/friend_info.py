from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class GetStrangerInfo(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            user_id: int
            nickname: str
            sex: str
            age: int
            qid: str
            level: int
            login_days: int

        data: Data

    action = "get_stranger_info"

    def __init__(self, user_id: int, no_cache: bool = False, *, echo: str = ""):
        self.user_id = user_id
        self.echo = echo


@register_to_api
class GetFriendList(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            user_id: int
            nickname: str
            remark: str

        data: Data

    action = "get_friend_list"

    def __init__(self, *, echo: str = ""):
        self.echo = echo


@register_to_api
class GetUnidirectionalFriendList(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            user_id: int
            nickname: str
            source: str

    action = "get_unidirectional_friend_list"

    def __init__(self, *, echo: str = ""):
        self.echo = echo
