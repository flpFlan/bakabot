import re
from inspect import getfullargspec
from types import NoneType
from typing import ClassVar, Type, TypeVar, Generic, get_type_hints, get_args, overload
from dataclasses import dataclass
from cqhttp.events.message import Message
from utils.algorithm import first


@dataclass(repr=False)
class _CQCode:
    cq: str = ""


_CQ = TypeVar("_CQ", bound=_CQCode)


class CQCode(_CQCode, Generic[_CQ]):
    classes:ClassVar[set[Type["CQCode"]]] = set()

    pattern:re.Pattern[str]

    def __init_subclass__(cls):
        cq = cls.cq or r"[^\d\s]+?"
        cls.pattern = re.compile(rf"\[CQ:{cq},(?P<params>(?:[^\d\s\[\]]+=[^,\s\[\]]+)+?)\]")
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

    @overload
    @classmethod
    def select_from(cls, msg: str) -> list[_CQ] | None:...

    @overload
    @classmethod
    def select_from(cls, msg: Message) -> list[_CQ] | None:...
    
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
    
    @overload
    @classmethod
    def exist_in(cls, msg: Message) -> bool:...

    @overload
    @classmethod
    def exist_in(cls, msg: str) -> bool:...

    def __str__(self) -> str:
        if params := (f"{k}={v}" if v else "" for k, v in vars(self).items()):
            params = ",".join(params)
            return f"[CQ:{self.cq},{params}]"
        else:
            return f"[CQ:{self.cq}]"

    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, o: object) -> bool:...

    def __add__(self, o: object) -> str:...

    def __sub__(self, o: object) -> str:...


def register_to_cqcodes(cls):
    CQCode.classes.add(cls)
    return cls
