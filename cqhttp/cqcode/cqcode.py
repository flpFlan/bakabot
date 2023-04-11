from cqhttp import cqcode
from .base import CQCode, register_to_cqcodes


@register_to_cqcodes
class Face(CQCode):
    """QQ 表情"""

    cq = "face"
    id: str


@register_to_cqcodes
class Record(CQCode):
    """语音"""

    cq = "record"
    file: str
    magic: str
    url: str


@register_to_cqcodes
class Video(CQCode):
    """短视频"""

    cq = "video"

    file: str
    cover: str
    c: str


@register_to_cqcodes
class At(CQCode):
    """@某人"""

    cq = "at"

    qq: str


@register_to_cqcodes
class RPS(CQCode):
    """猜拳魔法表情"""

    cq = "rps"


@register_to_cqcodes
class Dice(CQCode):
    """掷骰子魔法表情"""

    cq = "dice"


@register_to_cqcodes
class Share(CQCode):
    """链接分享"""

    cq = "share"
    url: str
    title: str
    content: str
    image: str


@register_to_cqcodes
class Contact(CQCode):
    """推荐好友/群"""

    cq = "contact"
    type: str
    id: str


@register_to_cqcodes
class Location(CQCode):
    """位置"""

    cq = "location"
    lat: str
    lon: str
    title: str
    content: str


@register_to_cqcodes
class Image(CQCode):
    """图片"""

    cq = "iamge"
    file: str
    type: str
    subType: str
    url: str
    id: str


@register_to_cqcodes
class Reply(CQCode):
    """回复"""

    cq = "reply"
    id: str
    text: str
    qq: str
    time: str
    seq: str


@register_to_cqcodes
class RedBag(CQCode):
    """红包"""

    cq = "redbag"
    title: str


@register_to_cqcodes
class Forward(CQCode):
    """合并转发"""

    cq = "forward"
    id: str


@register_to_cqcodes
class XML(CQCode):
    """XML 消息"""

    cq = "xml"
    data: str
    resid: str | None


@register_to_cqcodes
class Json(CQCode):
    """JSON 消息"""

    cq = "json"
    data: str
