# -- stdlib --
from typing import Type
from collections import defaultdict

# -- third party --
# -- own --
from cqhttp.base import Event, EventArgs

# -- code --


class CQHTTPEventArgs(EventArgs):
    ...


class CQHTTPEvent(Event):
    time: int
    self_id: int
    post_type: str

    def __init__(self):
        self._ = CQHTTPEventArgs()


def nested_dict():
    return defaultdict(nested_dict)


all_events = nested_dict()


def register_to_events(evt: Type[CQHTTPEvent]):
    st = getattr(evt, "sub_type", None)
    if mt := getattr(evt, "message_type", None):
        if st:
            all_events["message"][mt][st] = evt
        else:
            all_events["message"][mt][" "] = evt
    elif nt := getattr(evt, "notice_type", None):
        if st:
            all_events["notice"][nt][st] = evt
        else:
            all_events["notice"][nt][" "] = evt
    elif rt := getattr(evt, "request_type", None):
        if st:
            all_events["request"][rt][st] = evt
        else:
            all_events["request"][rt][" "] = evt
    elif met := getattr(evt, "meta_event_type", None):
        if st:
            all_events["meta_event"][met][st] = evt
        else:
            all_events["meta_event"][met][" "] = evt
    else:
        raise Exception("post_type error")
    return evt
