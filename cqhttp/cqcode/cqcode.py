from dataclasses import dataclass, field
from typing import ClassVar, Optional
from .base import CQCode, CQCodeData, register_to_cqcodes


@dataclass(repr=False)
class _FaceData(CQCodeData):
    cq: ClassVar[str] = "face"
    id: int


@register_to_cqcodes
class Face(_FaceData, CQCode[_FaceData]):
    """QQ 表情"""


@dataclass(repr=False)
class _RecordData(CQCodeData):
    cq: ClassVar[str] = "record"
    file: str = field()
    url: str = field(init=False)
    magic: int = field(default=0)
    cache: int = field(default=1)
    proxy: int = field(default=1)
    timeout: Optional[int] = field(default=None)


@register_to_cqcodes
class Record(_RecordData, CQCode[_RecordData]):
    """语音"""


@dataclass(repr=False)
class _VideoData(CQCodeData):
    cq: ClassVar[str] = "video"
    file: str = field()
    cover: str = field()
    c: Optional[int] = field(default=None)


@register_to_cqcodes
class Video(_VideoData, CQCode[_VideoData]):
    """短视频"""


@dataclass(repr=False)
class _AtData(CQCodeData):
    cq: ClassVar[str] = "at"
    qq: int = field()
    name: str = field(init=False)


@register_to_cqcodes
class At(_AtData, CQCode[_AtData]):
    """@某人"""


@dataclass(repr=False)
class _RPSData(CQCodeData):
    cq: ClassVar[str] = "rps"


@register_to_cqcodes
class RPS(_RPSData, CQCode[_RPSData]):
    """猜拳魔法表情"""


@dataclass(repr=False)
class _DiceData(CQCodeData):
    cq: ClassVar[str] = "dice"


@register_to_cqcodes
class Dice(_DiceData, CQCode[_DiceData]):
    """掷骰子魔法表情"""


@dataclass(repr=False)
class _ShakeData(CQCodeData):
    cq: ClassVar[str] = "shake"


@register_to_cqcodes
class Shake(_ShakeData, CQCode[_ShakeData]):
    """窗口抖动（戳一戳）"""


@dataclass(repr=False)
class _AnonymousData(CQCodeData):
    cq: ClassVar[str] = "anonymous"
    ignore: Optional[int] = field(default=None)


@register_to_cqcodes
class Anonymous(_AnonymousData, CQCode[_AnonymousData]):
    """匿名发消息"""


@dataclass(repr=False)
class _ShareData(CQCodeData):
    cq: ClassVar[str] = "share"
    url: str = field()
    title: str = field()
    content: Optional[str] = field(default=None)
    image: Optional[str] = field(default=None)


@register_to_cqcodes
class Share(_ShareData, CQCode[_ShareData]):
    """链接分享"""


@dataclass(repr=False)
class _ContactData(CQCodeData):
    cq: ClassVar[str] = "contact"
    type: str = field()
    id: str = field()


@register_to_cqcodes
class Contact(_ContactData, CQCode[_ContactData]):
    """推荐好友/群"""


@dataclass(repr=False)
class _LocationData(CQCodeData):
    cq: ClassVar[str] = "location"
    lat: str = field()
    lon: str = field()
    title: Optional[str] = field(default=None)
    content: Optional[str] = field(default=None)


@register_to_cqcodes
class Location(_LocationData, CQCode[_LocationData]):
    """位置"""


@dataclass(repr=False)
class _MusicData(CQCodeData):
    cq: ClassVar[str] = "music"
    type: str = field()
    id: int = field()


@register_to_cqcodes
class Music(_MusicData, CQCode[_MusicData]):
    """音乐分享"""


@dataclass(repr=False)
class _MusicCustomData(CQCodeData):
    cq: ClassVar[str] = "music"
    url: str = field()
    audio: str = field()
    title: str = field()
    content: Optional[str] = field(default=None)
    image: Optional[str] = field(default=None)
    type: str = field(default="custom")


@register_to_cqcodes
class MusicCustom(_MusicCustomData, CQCode[_MusicCustomData]):
    """音乐自定义分享"""


@dataclass(repr=False)
class _ImageData(CQCodeData):
    cq: ClassVar[str] = "image"
    file: str = field()
    type: Optional[str] = field(default=None)
    subType: Optional[int] = field(default=None)
    url: Optional[str] = field(default=None)
    cache: int = field(default=1)
    id: Optional[int] = field(default=None)
    c: Optional[int] = field(default=None)


@register_to_cqcodes
class Image(_ImageData, CQCode[_ImageData]):
    """图片"""


@dataclass(repr=False)
class _ReplyData(CQCodeData):
    cq: ClassVar[str] = "reply"
    id: int = field()
    seq: Optional[int] = field(default=None)


@register_to_cqcodes
class Reply(_ReplyData, CQCode[_ReplyData]):
    """回复"""


@dataclass(repr=False)
class _ReplyCustomData(CQCodeData):
    cq: ClassVar[str] = "reply"
    text: str = field()
    qq: int = field()
    time: int = field()
    seq: Optional[int] = field(default=None)


@register_to_cqcodes
class ReplyCustom(_ReplyCustomData, CQCode[_ReplyCustomData]):
    """自定义回复"""


@dataclass(repr=False)
class _RedBagData(CQCodeData):
    cq: ClassVar[str] = "redbag"
    title: str = field()


@register_to_cqcodes
class RedBag(_RedBagData, CQCode[_RedBagData]):
    """红包"""


@dataclass(repr=False)
class _PokeData(CQCodeData):
    cq: ClassVar[str] = "poke"
    qq: int = field()


@register_to_cqcodes
class Poke(_PokeData, CQCode[_PokeData]):
    """戳一戳"""


@dataclass(repr=False)
class _GiftData(CQCodeData):
    cq: ClassVar[str] = "gift"
    qq: int = field()
    id: int = field()


@register_to_cqcodes
class Gift(_GiftData, CQCode[_GiftData]):
    """礼物"""


@dataclass(repr=False)
class _ForwardData(CQCodeData):
    cq: ClassVar[str] = "forward"
    id: str = field()


@register_to_cqcodes
class Forward(_ForwardData, CQCode[_ForwardData]):
    """合并转发"""


@dataclass(repr=False)
class _NodeData(CQCodeData):
    cq: ClassVar[str] = "node"
    id: int = field()


@register_to_cqcodes
class Node(_NodeData, CQCode[_NodeData]):
    """合并转发消息节点"""


@dataclass(repr=False)
class _NodeCustomData(CQCodeData):
    cq: ClassVar[str] = "node"
    name: str = field()
    uin: int = field()
    content: Optional[str] = field(default=None)
    seq: Optional[str] = field(default=None)


@register_to_cqcodes
class NodeCustom(_NodeCustomData, CQCode[_NodeCustomData]):
    """合并转发消息节点(自定义)"""


@dataclass(repr=False)
class _XMLData(CQCodeData):
    cq: ClassVar[str] = "xml"
    data: str = field()
    resid: Optional[int] = field(default=None)


@register_to_cqcodes
class XML(_XMLData, CQCode[_XMLData]):
    """XML 消息"""


@dataclass(repr=False)
class _JsonData(CQCodeData):
    cq: ClassVar[str] = "json"
    data: str = field()
    resid: Optional[int] = field(default=None)


@register_to_cqcodes
class Json(_JsonData, CQCode[_JsonData]):
    """JSON 消息"""


@dataclass(repr=False)
class _CardImageData(CQCodeData):
    cq: ClassVar[str] = "cardimage"
    file: str = field()
    minwidth: Optional[int] = field(default=None)
    minheight: Optional[int] = field(default=None)
    maxwidth: Optional[int] = field(default=None)
    maxheight: Optional[int] = field(default=None)
    source: Optional[str] = field(default=None)
    icon: Optional[str] = field(default=None)


@register_to_cqcodes
class CardImage(_CardImageData, CQCode[_CardImageData]):
    """cardimage"""


@dataclass(repr=False)
class _TTSData(CQCodeData):
    cq: ClassVar[str] = "tts"
    text: str = field()


@register_to_cqcodes
class TTS(_TTSData, CQCode[_TTSData]):
    """文本转语音"""
