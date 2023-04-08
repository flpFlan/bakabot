"""图片相关 API"""
from cqhttp.api.base import ApiAction, register_to_api


@register_to_api
class GetImage(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            size: int
            filename: str
            url: str

        data: Data

    action = "get_image"

    def __init__(self, file: str):
        self.file = file


@register_to_api
class CanSendImage(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            yes: bool

        data: Data

    action = "can_send_image"


@register_to_api
class OcrImage(ApiAction):
    class Response(ApiAction.Response):
        class Data:
            texts: list
            language: str

        data: Data

    action = "ocr_image"

    def __init__(self, image: str):
        self.image = image
