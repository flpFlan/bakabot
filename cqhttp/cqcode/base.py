import re
from inspect import getfullargspec
from types import NoneType
from typing import ClassVar, Type, TypeVar, Generic, get_type_hints, get_args, Self
from dataclasses import dataclass
from cqhttp.events.message import Message
from utils.algorithm import first


@dataclass(repr=False)
class CQCodeData:
    cq: ClassVar[str]


_CQ = TypeVar("_CQ", bound=CQCodeData)


class CQCode(CQCodeData, Generic[_CQ]):
    classes: ClassVar[set[Type["CQCode"]]] = set()
    pattern: ClassVar[re.Pattern[str]]

    def __init_subclass__(cls):
        cq = cls.cq or r"[^\d\s]+?"
        cls.pattern = re.compile(
            rf"\[CQ:{cq},(?P<params>(?:[^\d\s\[\]]+=[^,\s\[\]]+)+?)\]"
        )

    @classmethod
    def select_from(cls, msg: str | Message) -> list[Self] | None:
        if isinstance(msg, Message):
            msg = msg.message
        r = []
        for cqcode in cls.pattern.finditer(msg):
            params = {}

            for param in cqcode.group("params").split(","):
                key, value = param.split("=")
                t = get_type_hints(cls)[key]
                if hasattr(t, "__args__"):
                    t = first(get_args(t), lambda x: x is not NoneType)
                assert t
                params[key] = t(value)
            r.append(cls(**params))
        return r or None

    @classmethod
    def exist_in(cls, msg: Message | str) -> bool:
        if isinstance(msg, Message):
            msg = msg.message
        if cls.pattern.search(msg):
            return True
        return False
    
    def decode(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        gnrtor = (f"{k}={v}" if v is not None else "" for k, v in vars(self).items())
        if params_l := list(filter(lambda x: x != "", gnrtor)):
            params = ",".join(params_l)
            return f"[CQ:{self.cq},{params}]"
        else:
            return f"[CQ:{self.cq}]"

    def __repr__(self) -> str:
        return self.__str__()


def register_to_cqcodes(cls):
    CQCode.classes.add(cls)
    return cls
