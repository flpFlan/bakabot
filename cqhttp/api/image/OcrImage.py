"""图片 OCR"""
from typing import Optional
from cqhttp.api.base import ApiAction, register_to_api, ResponseBase


class Response(ResponseBase):
    class Data:
        class TextDetection:
            text: str
            confidence: int
            coordinates: list[int]

        texts: list[TextDetection]
        language: str

    data: Data


@register_to_api
class OcrImage(ApiAction[Response]):
    """图片 OCR"""

    action = "ocr_image"
    response = Response()

    def __init__(self, image: str, *, echo: Optional[str] = None):
        self.image = image
        self.echo = echo
