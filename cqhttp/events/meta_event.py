from cqhttp.events.base import CQHTTPEvent
from dataclasses import dataclass,field


@dataclass
class MetaEvent(CQHTTPEvent):
    post_type:str = "meta_event"

    meta_event_type: str = field(kw_only=True)


@CQHTTPEvent.register
@dataclass
class HeartBeatBag(MetaEvent):
    @dataclass
    class Status:
        @dataclass
        class StatusStatistics:
            PacketReceived: int = field(kw_only=True)
            PacketSent: int = field(kw_only=True)
            PacketLost: int = field(kw_only=True)
            MessageReceived: int = field(kw_only=True)
            MessageSent: int = field(kw_only=True)
            DisconnectTimes: int = field(kw_only=True)
            LostTimes: int = field(kw_only=True)
            LastMessageTime: int = field(kw_only=True)

        app_initialized: bool = field(kw_only=True)
        app_enabled: bool = field(kw_only=True)
        plugins_good: bool = field(kw_only=True)
        app_good: bool = field(kw_only=True)
        online: bool = field(kw_only=True)
        stat: StatusStatistics = field(kw_only=True)

    meta_event_type: str  = "heartbeat"

    status: Status = field(kw_only=True)
    interval: int = field(kw_only=True)


@dataclass
class LifeCycle(MetaEvent):
    meta_event_type:str = "lifecycle"

    sub_type: str = field(kw_only=True)


@CQHTTPEvent.register
@dataclass
class LifeCycleEnabled(LifeCycle):
    sub_type:str = "enable"


@CQHTTPEvent.register
@dataclass
class LifeCycleDisabled(LifeCycle):
    sub_type:str = "disable"


@CQHTTPEvent.register
@dataclass
class LifeCycleConnected(LifeCycle):
    sub_type:str = "connect"