from dataclasses import dataclass, field
from typing import Optional
from .base import CQCode, register_to_cqcodes


@dataclass(repr=False)
class Face:
    id: int
    cq = "face"


@register_to_cqcodes
class Face(Face, CQCode[Face]):
    """QQ 表情"""


@dataclass(repr=False)
class Record:
    file: str
    url: str = field(init=False)
    magic: int = 0
    cache: int = 1
    proxy: int = 1
    timeout: Optional[int] = None
    cq = "record"


@register_to_cqcodes
class Record(Record, CQCode[Record]):
    """语音"""


@dataclass(repr=False)
class Video:
    file: str
    cover: str
    c: Optional[int] = None
    cq = "video"


@register_to_cqcodes
class Video(Video, CQCode[Video]):
    """短视频"""


@dataclass(repr=False)
class At:
    qq: int
    name: str = field(init=False)
    cq = "at"


@register_to_cqcodes
class At(At, CQCode[At]):
    """@某人"""


@dataclass(repr=False)
class RPS:
    cq = "rps"


@register_to_cqcodes
class RPS(RPS, CQCode[RPS]):
    """猜拳魔法表情"""


@dataclass(repr=False)
class Dice:
    cq = "dice"


@register_to_cqcodes
class Dice(Dice, CQCode[Dice]):
    """掷骰子魔法表情"""


@dataclass(repr=False)
class Shake:
    cq = "shake"


@register_to_cqcodes
class Shake(Shake, CQCode[Shake]):
    """窗口抖动（戳一戳）"""


@dataclass(repr=False)
class Anonymous:
    ignore: Optional[int] = None
    cq = "anonymous"


@register_to_cqcodes
class Anonymous(Anonymous, CQCode[Anonymous]):
    """匿名发消息"""


@dataclass(repr=False)
class Share:
    url: str
    title: str
    content: Optional[str] = None
    image: Optional[str] = None
    cq = "share"


@register_to_cqcodes
class Share(Share, CQCode[Share]):
    """链接分享"""


@dataclass(repr=False)
class Contact:
    type: str
    id: str
    cq = "contact"


@register_to_cqcodes
class Contact(Contact, CQCode[Contact]):
    """推荐好友/群"""


@dataclass(repr=False)
class Location:
    lat: str
    lon: str
    title: Optional[str] = None
    content: Optional[str] = None
    cq = "location"


@register_to_cqcodes
class Location(Location, CQCode[Location]):
    """位置"""


@dataclass(repr=False)
class Music:
    type: str
    id: int
    cq = "music"


@register_to_cqcodes
class Music(Music, CQCode[Music]):
    """音乐分享"""


@dataclass(repr=False)
class MusicCustom:
    url: str
    audio: str
    title: str
    content: Optional[str] = None
    image: Optional[str] = None
    type: str = "custom"
    cq = "music"


@register_to_cqcodes
class MusicCustom(MusicCustom, CQCode[MusicCustom]):
    """音乐自定义分享"""


@dataclass(repr=False)
class Image:
    file: str
    type: Optional[str] = None
    subType: Optional[int] = None
    url: Optional[str] = None
    cache: int = 1
    id: Optional[int] = None
    c: Optional[int] = None
    cq = "iamge"


@register_to_cqcodes
class Image(Image, CQCode[Image]):
    """图片"""


@dataclass(repr=False)
class Reply:
    id: int
    seq: Optional[int] = None
    cq = "reply"


@register_to_cqcodes
class Reply(Reply, CQCode[Reply]):
    """回复"""


@dataclass(repr=False)
class ReplyCustom:
    text: str
    qq: int
    time: int
    seq: Optional[int] = None
    cq = "reply"


@register_to_cqcodes
class ReplyCustom(ReplyCustom, CQCode[ReplyCustom]):
    """自定义回复"""


@dataclass(repr=False)
class RedBag:
    title: str
    cq = "redbag"


@register_to_cqcodes
class RedBag(RedBag, CQCode[RedBag]):
    """红包"""


@dataclass(repr=False)
class Poke:
    qq: int
    cq = "poke"


@register_to_cqcodes
class Poke(Poke, CQCode[Poke]):
    """戳一戳"""


@dataclass(repr=False)
class Gift:
    qq: int
    id: int
    cq = "gift"


@register_to_cqcodes
class Gift(Gift, CQCode[Gift]):
    """礼物"""


@dataclass(repr=False)
class Forward:
    id: str
    cq = "forward"


@register_to_cqcodes
class Forward(Forward, CQCode[Forward]):
    """合并转发"""


@dataclass(repr=False)
class Node:
    id: int
    cq = "node"


@register_to_cqcodes
class Node(Node, CQCode[Node]):
    """合并转发消息节点"""


@dataclass(repr=False)
class NodeCustom:
    name: str
    uin: int
    content: Optional[str] = None
    seq: Optional[str] = None
    cq = "node"


@register_to_cqcodes
class NodeCustom(NodeCustom, CQCode[NodeCustom]):
    """合并转发消息节点(自定义)"""


@dataclass(repr=False)
class XML:
    data: str
    resid: Optional[int] = None
    cq = "xml"


@register_to_cqcodes
class XML(XML, CQCode[XML]):
    """XML 消息"""


@dataclass(repr=False)
class Json:
    data: str
    resid: Optional[int] = None
    cq = "json"


@register_to_cqcodes
class Json(Json, CQCode[Json]):
    """JSON 消息"""


@dataclass(repr=False)
class CardImage:
    file: str
    minwidth: Optional[int] = None
    minheight: Optional[int] = None
    maxwidth: Optional[int] = None
    maxheight: Optional[int] = None
    source: Optional[str] = None
    icon: Optional[str] = None
    cq = "cardimage"


@register_to_cqcodes
class CardImage(CardImage, CQCode[CardImage]):
    """cardimage"""


@dataclass(repr=False)
class TTS:
    text: str
    cq = "tts"


@register_to_cqcodes
class TTS(TTS, CQCode[TTS]):
    """文本转语音"""
