# -- stdlib --
import asyncio
from asyncio import Queue
import inspect
import logging
from re import Match, compile, RegexFlag
from collections import defaultdict
from typing import Callable, ClassVar, Coroutine, Generic, List, Literal, Self
from typing import Tuple, Type, TypeVar
from typing import TYPE_CHECKING, get_args, overload, DefaultDict

# -- own --
from accio import ACCIO
from cqhttp.api.base import ApiAction, ResponseBase
from cqhttp.events.base import CQHTTPEvent

# -- code --

if TYPE_CHECKING:
    from cqhttp.events.message import Message

log = logging.getLogger("bot.service")

_TCQHTTPEvent = TypeVar("_TCQHTTPEvent", bound=CQHTTPEvent)
_TApiAction = TypeVar("_TApiAction", bound=ApiAction)
_TServiceBehavior = TypeVar("_TServiceBehavior", bound="ServiceBehavior")
_TResponse = TypeVar("_TResponse", bound=ResponseBase)

_A = tuple[ApiAction, Literal[False], ResponseBase]
_B = tuple[ApiAction, Literal[True], Literal[None]]
_A_Class_Handler = Callable[
    [_TServiceBehavior, _TApiAction, _TResponse], Coroutine[None, None, None]
]
_B_Class_Handler = Callable[
    [_TServiceBehavior, _TApiAction], Coroutine[None, None, None]
]
_C_Class_Handler = Callable[
    [_TServiceBehavior, _TCQHTTPEvent], Coroutine[None, None, None]
]
_A_Handler = Callable[[_TApiAction, _TResponse], Coroutine[None, None, None]]
_B_Handler = Callable[[_TApiAction], Coroutine[None, None, None]]
_C_Handler = Callable[[_TCQHTTPEvent], Coroutine[None, None, None]]


class Service:
    name: ClassVar[str] = ""
    descrition: ClassVar[str] = ""
    behaviors: ClassVar[
        list[Type["ServiceBehavior"]]
    ]  # override it to make behaviors sync

    def __init_subclass__(cls):
        cls.name = cls.name or cls.__name__
        cls.descrition = cls.descrition or cls.__doc__ or ""

    def __init__(self):
        """Service cann't be instantiated directly, use Service.create_instance instead"""
        assert inspect.stack()[1][3] == "create_instance"
        cls = self.__class__
        if not hasattr(cls, "behaviors"):
            cls.behaviors = []
        self._behaviors: list[ServiceBehavior[Self]] = []
        self._evt_queue: Queue[CQHTTPEvent | _A | _B] = Queue()
        self._active = False

    def feed(self, evt: CQHTTPEvent | _A | _B):
        if self._active:
            self._evt_queue.put_nowait(evt)

    async def loop(self):
        while True:
            evt = await self._evt_queue.get()
            _t = asyncio.create_task(self.handle(evt))

    async def handle(self, evt: CQHTTPEvent | _A | _B):
        for behavior in self._behaviors:  # NOTE: must be sync
            if behavior.get_activity():
                await behavior._handle(evt)

    def get_activity(self):
        return self._active

    def get_behaviors(self):
        return self._behaviors

    def add_behavior(self, behavior: "ServiceBehavior"):
        self._behaviors.append(behavior)

    async def start(self):
        db = ACCIO.db
        service = self.__class__.__name__
        db.execute(
            """
            insert or replace into services (service,service_on) values (?,?)
            """,
            (service, True),
        )
        for bhv in self._behaviors:
            bhv.set_activity(True)

        self._l = asyncio.create_task(self.loop())
        self._active = True

    async def shutdown(self):
        db = ACCIO.db
        service = self.__class__.__name__
        db.execute(
            "insert or replace into services (service,service_on) values (?,?)",
            (service, False),
        )
        for bhv in self._behaviors:
            bhv.set_activity(False)

        # TODO: better way to cancel
        self._l.cancel()
        self._active = False

    async def __setup(self):
        ...  # to override it

    @classmethod
    def get_classes(cls) -> list[Type["Service"]]:
        subs = []
        for sub in cls.__subclasses__():
            subs.append(sub)
            if c := sub.get_classes():
                subs.extend(c)
        return subs

    @classmethod
    async def create_instance(cls):
        self = cls()
        # TODO
        if __setup := getattr(self, f"_{self.__class__.__name__}__setup", None):
            await __setup()  # NOTE: ensure all services were instantiated before setup
        self._behaviors = [
            await behavior.create_instance(self) for behavior in cls.behaviors
        ]
        return self


_TService = TypeVar("_TService", bound=Service)


class ServiceBehavior(Generic[_TService]):
    def __init_subclass__(cls):
        service_t = get_args(cls.__orig_bases__[0])[0]  # type: ignore
        assert not hasattr(service_t, "__args__")  # cann't be union
        assert issubclass(service_t, Service)
        if not service_t.__dict__.get("behaviors"):
            service_t.behaviors = []
        if not cls in service_t.behaviors:
            service_t.behaviors.append(cls)

    def __init__(self, service: _TService):
        """ServiceBehavior cann't be instantiated directly, use ServiceBehavior.create_instance instead"""
        cqevt_handlers = defaultdict(list)
        act_before_handlers = defaultdict(list)
        act_after_handlers = defaultdict(list)
        for _, f in inspect.getmembers(self, inspect.isroutine):
            if evt_ts := getattr(f, "cqevt_entrypoint", None):
                for evt_t in evt_ts:
                    if issubclass(evt_t, CQHTTPEvent):
                        cqevt_handlers[evt_t].append(f)
            elif evt_ts := getattr(f, "act_before_entrypoint", None):
                for evt_t in evt_ts:
                    if issubclass(evt_t, ApiAction):
                        act_before_handlers[evt_t].append(f)
            elif evt_ts := getattr(f, "act_after_entrypoint", None):
                for evt_t in evt_ts:
                    if issubclass(evt_t, ApiAction):
                        act_after_handlers[evt_t].append(f)
        self._cqevt_handlers: DefaultDict[
            Type[CQHTTPEvent], List[_C_Handler]
        ] = cqevt_handlers
        self._act_after_handlers: DefaultDict[
            Type[ApiAction], List[_A_Handler]
        ] = act_after_handlers
        self._act_before_handlers: DefaultDict[
            Type[ApiAction], List[_B_Handler]
        ] = act_before_handlers
        self.service = service
        self.set_activity(False)

    def set_activity(self, active: bool):
        self._active = active

    def get_activity(self):
        return self._active

    @overload
    async def _handle(self, evt: CQHTTPEvent):
        ...

    @overload
    async def _handle(self, evt: _A):
        ...

    @overload
    async def _handle(self, evt: _B):
        ...

    async def _handle(self, evt: CQHTTPEvent | _A | _B):
        if isinstance(evt, CQHTTPEvent):
            t = [asyncio.create_task(f(evt)) for f in self._cqevt_handlers[evt.__class__]]
        else:
            e, before_post, arg = evt
            if before_post:
                t = [asyncio.create_task(f(e)) for f in self._act_before_handlers[e.__class__]]
            else:
                assert arg
                t = [asyncio.create_task(f(e, arg)) for f in self._act_after_handlers[e.__class__]]
        if t:
            await asyncio.wait(t)

    async def __setup(self):
        ...

    @classmethod
    async def create_instance(cls, service: _TService):
        self = cls(service)
        if isinstance(self, IMessageFilter):
            self.compile()
        if __setup := getattr(self, f"_{self.__class__.__name__}__setup", None):
            await __setup()
        return self


class EventHub:
    pass


class CQHTTPEventHub(EventHub, Generic[_TCQHTTPEvent]):
    _type: Tuple[Type[_TCQHTTPEvent], ...]

    def __class_getitem__(cls, item):
        cls._type = item
        return cls

    @staticmethod
    def add_listener(f: _C_Class_Handler):
        attr_old = getattr(f, "cqevt_entrypoint", ())
        attr_new: set[Type[CQHTTPEvent]] = set([*CQHTTPEventHub._type, *attr_old])
        real_types = set()
        for evt_t in attr_new:
            for e in evt_t.get_real_types():
                real_types.add(e)
        setattr(f, "cqevt_entrypoint", tuple(real_types))
        return f


_TApiActionT = TypeVar("_TApiActionT", bound=ApiAction)


class ApiActionHub(EventHub, Generic[_TApiAction]):
    _type: Tuple[Type[_TApiAction], ...]

    def __class_getitem__(cls, item):
        cls._type = item
        return cls

    class _BeforePost(Generic[_TApiActionT]):
        @staticmethod
        def add_listener(f: _B_Class_Handler):
            attr_old = getattr(f, "act_before_entrypoint", ())
            attr_new: set[Type[ApiAction]] = set([*ApiActionHub._type, *attr_old])
            real_types = set()
            for evt_t in attr_new:
                for e in evt_t.get_real_types():
                    real_types.add(e)
            setattr(f, "act_before_entrypoint", tuple(real_types))
            return f

    class _AfterPost(Generic[_TApiActionT]):
        @staticmethod
        def add_listener(f: _A_Class_Handler):
            attr_old = getattr(f, "act_after_entrypoint", ())
            attr_new: set[Type[ApiAction]] = set([*ApiActionHub._type, *attr_old])
            real_types = set()
            for evt_t in attr_new:
                for e in evt_t.get_real_types():
                    real_types.add(e)
            setattr(f, "act_after_entrypoint", tuple(real_types))
            return f

    @staticmethod
    def before_post():
        return ApiActionHub._BeforePost[_TApiAction]

    @staticmethod
    def after_post():
        return ApiActionHub._AfterPost[_TApiAction]


class _META(type):
    @overload
    def __getitem__(
        cls, evts_t: Type[_TCQHTTPEvent]
    ) -> Type[CQHTTPEventHub[_TCQHTTPEvent]]:
        ...

    @overload
    def __getitem__(
        cls, evts_t: Tuple[Type[_TCQHTTPEvent], ...]
    ) -> Type[CQHTTPEventHub[_TCQHTTPEvent]]:
        ...

    @overload
    def __getitem__(cls, evts_t: Type[_TApiAction]) -> Type[ApiActionHub[_TApiAction]]:
        ...

    @overload
    def __getitem__(
        cls, evts_t: Tuple[Type[_TApiAction], ...]
    ) -> Type[ApiActionHub[_TApiAction]]:
        ...

    def __getitem__(cls, evts_t):
        _evts_t = get_args(evts_t) or evts_t
        if not isinstance(_evts_t, tuple):
            _evts_t = (_evts_t,)
        for evt_t in _evts_t:
            if issubclass(evt_t, CQHTTPEvent):
                return CQHTTPEventHub[_evts_t]  # type: ignore
            elif issubclass(evt_t, ApiAction):
                return ApiActionHub[_evts_t]  # type: ignore
            else:
                raise TypeError("evts_t must be subclass of CQHTTPEvent or ApiAction")


class OnEvent(metaclass=_META):
    pass


class IMessageFilter:
    entrys = []
    entry_flags = RegexFlag.NOFLAG

    def compile(self):
        cls = self.__class__
        cls.entrys = [compile(et, cls.entry_flags) for et in cls.entrys]

    # TODO: optimize
    def filter(self, evt: "Message") -> Match[str] | None:
        msg = evt.message
        for _entry in self.entrys:
            if match := _entry.match(msg):
                return match


# TODO
# def on_event(*evts_t:Type[Event]):
#     real_types=set()
#     for evt_t in evts_t:
#         for e in evt_t.get_real_types():
#             real_types.add(e)
#     def decorator(f):
#         for evt_t in real_types:
#             ...
#         return f
#     return decorator
