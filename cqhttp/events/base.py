# -- stdlib --
from collections import defaultdict
from dataclasses import dataclass,field

# -- third party --
# -- own --
from cqhttp.base import Event

# -- code --

def nested_dict():
    return defaultdict(nested_dict)

@dataclass
class CQHTTPEvent(Event):
    classes=nested_dict()

    post_type: str=field(kw_only=True)
    time: int=field(kw_only=True)
    self_id: int=field(kw_only=True)

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
