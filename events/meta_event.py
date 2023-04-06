from events.base import CQHTTPEvent


class MetaEvent(CQHTTPEvent):
    post_type = "meta_event"
    meta_event_type: str


class HeartBeatBag(MetaEvent):
    meta_event_type: str = "heartbeat"

    status: dict
    interval: int


class LifeCycle(MetaEvent):
    meta_event_type = "lifecycle"

    sub_type: str


class LifeCycleEnabled(LifeCycle):
    sub_type = "enable"


class LifeCycleDisabled(LifeCycle):
    sub_type = "disable"


class LifeCycleConnected(LifeCycle):
    sub_type = "connect"
