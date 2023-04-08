"""语音相关 API"""
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class GetRecord(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            file: str

        data: Data

    action = "get_record"

    def __init__(self, file: str, out_format: str):
        self.file = file
        self.out_format = out_format


@register_to_api
class CanSendRecord(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            yes: bool

        data: Data

    action = "can_send_record"
