# -- stdlib --
from collections import defaultdict
from typing import ClassVar, Type, Self
from abc import ABC

# -- third party --
# -- own --
from cqhttp.base import Event

# -- code --


def nested_dict():
    return defaultdict(nested_dict)


class DotDict:
    def __init__(self, d: dict):
        self.__model = d

    def __getattr__(self, name):
        item = self.__model.get(name)  # NOTE:考虑到Optional字段，这里用get而不是下标
        if isinstance(item, dict):
            item = DotDict(item)
        elif isinstance(item, list):
            item = [DotDict(i) if isinstance(i, dict) else i for i in item]
        setattr(self, name, item)
        return item


class CQHTTPEvent(Event, DotDict, ABC):
    classes: ClassVar[dict] = nested_dict() # type: ignore

    post_type: str
    time: int
    self_id: int

    def cancel(self):
        self.__class__ = EmptyCQHTTPEvent

    @staticmethod
    def register(evt):
        st = getattr(evt, "sub_type", None)
        if mt := getattr(evt, "message_type", None):
            if st:
                CQHTTPEvent.classes["message"][mt][st] = evt
            else:
                CQHTTPEvent.classes["message"][mt][" "] = evt
        elif nt := getattr(evt, "notice_type", None):
            if st:
                CQHTTPEvent.classes["notice"][nt][st] = evt
            else:
                CQHTTPEvent.classes["notice"][nt][" "] = evt
        elif rt := getattr(evt, "request_type", None):
            if st:
                CQHTTPEvent.classes["request"][rt][st] = evt
            else:
                CQHTTPEvent.classes["request"][rt][" "] = evt
        elif met := getattr(evt, "meta_event_type", None):
            if st:
                CQHTTPEvent.classes["meta_event"][met][st] = evt
            else:
                CQHTTPEvent.classes["meta_event"][met][" "] = evt
        else:
            raise Exception("post_type error")
        Event.classes.add(evt)
        return evt

    @classmethod
    def get_real_types(cls) -> list[Type[Self]]:
        """get sub_events that can be actually delivered by go-cqhttp"""
        subs = []
        if cls in Event.classes:
            subs.append(cls)
        for sub in cls.__subclasses__():
            if sub in Event.classes:
                subs.append(sub)
            elif c := sub.get_real_types():
                subs.extend(c)
        return subs


class EmptyCQHTTPEvent(CQHTTPEvent):
    pass
