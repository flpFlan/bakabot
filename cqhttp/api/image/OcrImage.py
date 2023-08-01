"""图片 OCR"""
from dataclasses import dataclass, field
from typing import TypedDict
from cqhttp.api.base import ApiAction,  ResponseBase

class TextDetection(TypedDict):
    text: str
    confidence: int
    coordinates: list[int]
    
class Data(TypedDict):
    texts: list[TextDetection]
    language: str

class Response(ResponseBase):
    data: Data


@ApiAction.register
@dataclass
class OcrImage(ApiAction[Response]):
    """图片 OCR"""

    action:str = field(init=False,default="ocr_image")
    image: str
