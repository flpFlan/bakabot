import re
from inspect import getfullargspec
from types import NoneType
from typing import TypeVar, Generic, get_type_hints, get_args
from dataclasses import dataclass
from cqhttp.events.message import Message
from utils.algorithm import first


@dataclass(repr=False)
class _CQCode:
    cq: str = ""


_CQ = TypeVar("_CQ", bound=_CQCode)


class CQCode(_CQCode, Generic[_CQ]):
    def __init_subclass__(cls):
        cq = cls.cq or r"[^\d\s]+?"
        cls.pattern = re.compile( # type: ignore
            rf"\[CQ:{cq},(?P<params>(?:[^\d\s\[\]]+=[^,\s\[\]]+)+?)\]"
        )
        params = ",".join(getfullargspec(cls.__init__).args) # type: ignore
        env = {"i": cls.__init__} # type: ignore
        code = f"""
def __init__({params},**kargs):
    i({params})               
    for k,v in kargs.items(): 
        setattr(self,k,v)
""".strip()
        exec(code, env)
        cls.__init__ = env["__init__"] # type: ignore

    @classmethod
    def select_from(cls, msg: str | Message) -> list[_CQ] | None:
        if isinstance(msg, Message):
            msg = msg.message
        r = []
        for cqcode in cls.pattern.finditer(msg): # type: ignore
            params = {}

            for param in cqcode.group("params").split(","):
                key, value = param.split("=")
                t = get_type_hints(cls)[key]
                if hasattr(t, "__args__"):
                    t = first(get_args(t), lambda x: x is not NoneType)
                params[key] = t(value)
            r.append(cls(**params))
        return r or None

    def __str__(self) -> str:
        if params := (f"{k}={v}" if v else "" for k, v in vars(self).items()):
            params = ",".join(params)
            return f"[CQ:{self.cq},{params}]"
        else:
            return f"[CQ:{self.cq}]"

    def __repr__(self) -> str:
        return self.__str__()


all_cqcodes = set()


def register_to_cqcodes(cls):
    all_cqcodes.add(cls)
    return cls
