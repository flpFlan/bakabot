"""群信息相关 API"""
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class GetGroupInfo(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            group_id: int
            group_name: str
            group_memo: str
            group_create_time: int
            group_level: int
            member_count: int
            max_member_count: int

        data: Data

    action = "get_group_info"

    def __init__(self, group_id: int, no_cache: bool = False, *, echo: str = ""):
        self.group_id = group_id
        self.no_cache = no_cache
        self.echo = echo


@register_to_api
class GetGroupList(ApiAction):
    class Response(ApiAction.Response):
        data: list

    action = "get_group_list"

    def __init__(self, no_cache: bool = False, *, echo: str = ""):
        self.no_cache = no_cache
        self.echo = echo


@register_to_api
class GetGroupMemberInfo(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            group_id: int
            user_id: int
            nickname: str
            card: str
            sex: str
            age: int
            area: str
            join_time: int
            last_sent_time: int
            level: str
            role: str
            unfriendly: bool
            title: str
            title_expire_time: int
            card_changeable: bool
            shut_up_timestamp: int

        data: Data

    action = "get_group_member_info"

    def __init__(
        self, group_id: int, user_id: int, no_cache: bool = False, *, echo: str = ""
    ):
        self.group_id = group_id
        self.user_id = user_id
        self.no_cache = no_cache
        self.echo = echo


@register_to_api
class GetGroupMemberList(ApiAction):
    class Response(ApiAction.Response):
        data: list

    action = "get_group_member_list"

    def __init__(self, group_id: int, no_cache: bool = False, *, echo: str = ""):
        self.group_id = group_id
        self.no_cache = no_cache
        self.echo = echo


@register_to_api
class GetGroupHonorInfo(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            class CurrentTalkative:
                user_id: int
                nickname: str
                avatar: str
                day_count: int

            group_id: int
            current_talkative: CurrentTalkative
            talkative_list: list
            performer_list: list
            legend_list: list
            strong_newbie_list: list
            emotion_list: list

        data: Data

    action = "get_group_honor_info"

    def __init__(self, group_id: int, type: str, *, echo: str = ""):
        self.group_id = group_id
        self.type = type
        self.echo = echo


@register_to_api
class GetGroupSystemMsg(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            invited_requests: list
            join_requests: list

        data: Data

    action = "get_group_system_msg"

    def __init__(self, *, echo: str = ""):
        self.echo = echo


@register_to_api
class GetEssenceMsgList(ApiAction):
    class Response(ApiAction.Response):
        data: list

    action = "get_essence_msg_list"

    def __init__(self, group_id: int, *, echo: str = ""):
        self.group_id = group_id
        self.echo = echo


@register_to_api
class GetGroupAtAllRemain(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            can_at_all: bool
            remain_at_all_count_for_group: int
            remain_at_all_count_for_uin: int

        data: Data

    action = "get_group_at_all_remain"

    def __init__(self, group_id: int, *, echo: str = ""):
        self.group_id = group_id
        self.echo = echo
