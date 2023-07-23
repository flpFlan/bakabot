from cqhttp.events.base import CQHTTPEvent


class MetaEvent(CQHTTPEvent):
    post_type: str = "meta_event"

    meta_event_type: str


@CQHTTPEvent.register
class HeartBeatBag(MetaEvent):
    class Status:
        class StatusStatistics:
            packet_received: int
            packet_sent: int
            packet_lost: int
            message_received: int
            message_sent: int
            disconnect_times: int
            lost_times: int
            last_message_time: int

        app_initialized: bool
        app_enabled: bool
        plugins_good: bool
        app_good: bool
        online: bool
        stat: StatusStatistics

    meta_event_type: str = "heartbeat"

    status: Status
    interval: int


class LifeCycle(MetaEvent):
    meta_event_type: str = "lifecycle"

    sub_type: str


@CQHTTPEvent.register
class LifeCycleEnabled(LifeCycle):
    sub_type: str = "enable"


@CQHTTPEvent.register
class LifeCycleDisabled(LifeCycle):
    sub_type: str = "disable"


@CQHTTPEvent.register
class LifeCycleConnected(LifeCycle):
    sub_type: str = "connect"
