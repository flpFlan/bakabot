# -- stdlib --
import asyncio
from asyncio import Queue
import inspect
import logging
from re import compile
from collections import defaultdict
from typing import Callable, ClassVar, Coroutine, Generic, Optional
from typing import Tuple, Type, TypeVar
from typing import TYPE_CHECKING, cast, get_args, overload, DefaultDict


# -- third party --

# -- own --
from accio import ACCIO
from cqhttp.api.base import ApiAction, ResponseBase
from cqhttp.events.base import CQHTTPEvent
from services.base import ServiceBehavior

# -- code --

if TYPE_CHECKING:
    from cqhttp.events.message import Message

log = logging.getLogger("bot.service")


class Service:
    name: ClassVar[Optional[str]] = None
    behaviors: ClassVar[
        list[Type["ServiceBehavior"]]
    ]  # override it to make the behaviors sync

    def __init__(self):
        # Service cann't be instantiated directly, use Service.create_instance instead
        assert inspect.stack()[1][3] == "create_instance"
        cls = self.__class__
        if not hasattr(cls, "behaviors"):
            cls.behaviors = []
        self._behaviors = [behavior(self) for behavior in cls.behaviors]
        self._evt_queue: Queue[
            CQHTTPEvent | tuple[ApiAction, bool, Optional[dict]]
        ] = Queue()
        self._active = False

    async def feed(self, evt: CQHTTPEvent | tuple[ApiAction, bool, Optional[dict]]):
        if self._active:
            await self._evt_queue.put(evt)

    async def run(self):
        while True:
            evt = await self._evt_queue.get()
            for behavior in self._behaviors:  # must be sync
                if behavior.get_activity():
                    await behavior._handle(evt)

    def get_activity(self):
        return self._active

    def get_behaviors(self):
        return self._behaviors

    def add_behavior(self, behavior: "ServiceBehavior"):
        self._behaviors.append(behavior)

    async def start_up(self):
        db = ACCIO.db
        service = self.__class__.__name__
        db.execute(
            """
            insert or replace into services (service,service_on) values (?,?)
            """,
            (service, True),
        )
        for core in self._behaviors:
            core.set_activity(True)

        # TODO: add handlers
        for core in self._behaviors:
            ...
        self._r = asyncio.create_task(self.run())
        self._active = True

    async def shutdown(self):
        db = ACCIO.db
        service = self.__class__.__name__
        db.execute(
            "insert or replace into services (service,service_on) values (?,?)",
            (service, False),
        )
        db.commit()
        for core in self._behaviors:
            core.set_activity(False)

        # TODO: remove handlers
        for core in self._behaviors:
            ...
        self._r.cancel()
        self._active = False

    async def __setup(self):
        ...  # to override it

    @classmethod
    def get_classes(cls):
        subs = []
        for sub in cls.__subclasses__():
            subs.append(sub)
            if c := sub.get_classes():
                subs.extend(c)
        return subs

    @classmethod
    async def create_instance(cls):
        self = cls()
        await self.__setup()
        return self


_TService = TypeVar("_TService", bound=Service)


class ServiceBehavior(Generic[_TService]):
    def __init_subclass__(cls):
        service_t = get_args(cls.__orig_bases__[0])[0]  # type: ignore
        assert not hasattr(service_t, "__args__")  # cann't be union
        service_t = cast(Type[Service], service_t)
        if not hasattr(service_t, "behaviors"):
            service_t.behaviors = []
        if not cls in service_t.behaviors:
            service_t.behaviors.append(cls)

    def __init__(self, service: _TService):
        cq_evt_handlers = defaultdict(list)
        api_action_handlers = defaultdict(list)
        for f in inspect.getmembers(self, inspect.isroutine):
            if not (evts_t := getattr(f, "evt_entry_point", ())):
                continue
            for evt_t in evts_t:
                if isinstance(evt_t, CQHTTPEvent):
                    cq_evt_handlers[evt_t].append(f)
                elif isinstance(evt_t, ApiAction):
                    api_action_handlers[evt_t].append(f)
                else:
                    raise TypeError("WTF?!")
        self._cq_evt_handlers: DefaultDict[
            Type[CQHTTPEvent], list[Callable[[CQHTTPEvent], Coroutine]]
        ] = cq_evt_handlers
        self._api_action_handlers: DefaultDict[
            Type[ApiAction], list[Callable[[ApiAction], Coroutine]]
        ] = api_action_handlers
        self.service = service
        self.set_activity(False)

    def set_activity(self, active: bool):
        self._active = active

    def get_activity(self):
        return self._active

    async def _handle(self, evt: CQHTTPEvent | tuple[ApiAction, bool, Optional[dict]]):
        if isinstance(evt, CQHTTPEvent):
            asyncio.gather(*[f(evt) for f in self._cq_evt_handlers[evt.__class__]])
        elif isinstance(evt, tuple):
            e, before_post, arg = evt  # type: ignore
            if before_post:
                asyncio.gather(*[f(e) for f in self._api_action_handlers[e.__class__]])
            else:
                assert arg
                asyncio.gather(
                    *[f(e, arg) for f in self._api_action_handlers[e.__class__]]
                )
        else:
            raise TypeError("WTF?!")

    async def __setup(self):
        ...

    @classmethod
    async def create_instance(cls, service: _TService):
        self = cls(service)
        await self.__setup()
        return self


_TCQHTTPEvent = TypeVar("_TCQHTTPEvent", bound=CQHTTPEvent)
_TApiAction = TypeVar("_TApiAction", bound=ApiAction)
_TServiceBehavior = TypeVar("_TServiceBehavior", bound=ServiceBehavior)
_TResponse = TypeVar("_TResponse", bound=ResponseBase)


class EventHub:
    pass


class CQHTTPEventHub(EventHub, Generic[_TCQHTTPEvent]):
    _type: Tuple[_TCQHTTPEvent, ...]

    def __class_getitem__(cls, item):
        cls._type = item
        return cls

    @staticmethod
    def add_listener(
        f: Callable[[_TServiceBehavior, _TCQHTTPEvent], Coroutine[None, None, None]]
    ):
        attr_old = getattr(f, "evt_entry_point", ())
        attr_new: set[Type[CQHTTPEvent]] = set(*CQHTTPEventHub._type, *attr_old)
        real_types = set()
        for evt_t in attr_new:
            for e in evt_t.get_real_types():
                real_types.add(e)
        setattr(f, "evt_entry_point", tuple(real_types))
        return f


_TApiActionT = TypeVar("_TApiActionT", bound=ApiAction)


class ApiActionHub(EventHub, Generic[_TApiAction]):
    _type: Tuple[_TApiAction, ...]

    def __class_getitem__(cls, item):
        cls._type = item
        return cls

    class _BeforePost(Generic[_TApiActionT]):
        @staticmethod
        def add_listener(
            f: Callable[[_TServiceBehavior, _TApiActionT], Coroutine[None, None, None]]
        ):
            attr_old = getattr(f, "evt_entry_point", ())
            attr_new: set[Type[ApiAction]] = set(*ApiActionHub._type, *attr_old)  # type: ignore
            real_types = set()
            for evt_t in attr_new:
                for e in evt_t.get_real_types():
                    real_types.add(e)
            setattr(f, "evt_entry_point", tuple(real_types))
            return f

    class _AfterPost(Generic[_TApiActionT]):
        @staticmethod
        def add_listener(
            f: Callable[
                [_TServiceBehavior, _TApiActionT, _TResponse],
                Coroutine[None, None, None],
            ]
        ):
            attr_old = getattr(f, "evt_entry_point", ())
            attr_new: set[Type[ApiAction]] = set(*ApiActionHub._type, *attr_old)  # type: ignore
            real_types = set()
            for evt_t in attr_new:
                for e in evt_t.get_real_types():
                    real_types.add(e)
            setattr(f, "evt_entry_point", tuple(real_types))
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
    entry_flags = 0

    def __init_subclass__(cls):
        entry = cls.entrys
        cls.entrys = [compile(et, cls.entry_flags) for et in entry]

    def filter(self, evt: Message):
        msg = evt.message
        for _entry in self.entrys:
            if match := _entry.match(msg):
                return match.groupdict()


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
