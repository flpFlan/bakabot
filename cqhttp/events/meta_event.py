from cqhttp.events.base import CQHTTPEvent
from cqhttp.events.base import register_to_events


class MetaEvent(CQHTTPEvent):
    post_type = "meta_event"
    meta_event_type: str

    def __init__(self):
        super().__init__()


@register_to_events
class HeartBeatBag(MetaEvent):
    class Status:
        class StatusStatistics:
            PacketReceived: int
            PacketSent: int
            PacketLost: int
            MessageReceived: int
            MessageSent: int
            DisconnectTimes: int
            LostTimes: int
            LastMessageTime: int

        app_initialized: bool
        app_enabled: bool
        plugins_good: bool
        app_good: bool
        online: bool
        stat: StatusStatistics

    meta_event_type: str = "heartbeat"

    status: Status
    interval: int

    def __init__(self):
        super().__init__()


class LifeCycle(MetaEvent):
    meta_event_type = "lifecycle"

    sub_type: str

    def __init__(self):
        super().__init__()


@register_to_events
class LifeCycleEnabled(LifeCycle):
    sub_type = "enable"

    def __init__(self):
        super().__init__()


@register_to_events
class LifeCycleDisabled(LifeCycle):
    sub_type = "disable"

    def __init__(self):
        super().__init__()


@register_to_events
class LifeCycleConnected(LifeCycle):
    sub_type = "connect"

    def __init__(self):
        super().__init__()
