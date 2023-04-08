"""上报处理相关 API"""
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class SetFriendAddRequest(ApiAction):
    action = "set_friend_add_request"

    def __init__(
        self, flag: str, approve: bool = False, remark: str = "", *, echo: str = ""
    ):
        self.flag = flag
        self.approve = approve
        self.remark = remark
        self.echo = echo


@register_to_api
class SetGroupAddRequest(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            master_id: int
            ext_name: str
            create_time: int

        data: Data

    action = "set_group_add_request"

    def __init__(
        self,
        flag: str,
        sub_type: str,
        approve: bool = True,
        reason: str = "",
        *,
        echo: str = ""
    ):
        self.flag = flag
        self.sub_type = sub_type
        self.approve = approve
        self.reason = reason
        self.echo = echo
