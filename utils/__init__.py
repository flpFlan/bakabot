from threading import Timer
import time
from typing import Callable, Generic, Optional, TypeVar

T = TypeVar("T")


class ChronosItem(Generic[T]):
    def __init__(self, value: T, timeout: float, callback: Optional[Callable] = None):
        self._t = None
        self.timeout = timeout
        self._callback = callback
        self.__default_value = value
        self.value:T
        object.__setattr__(self,"value", value)

    @property
    def elapsed_time(self):
        if not self._t:
            return 0
        return time.time() - self._start_time

    def refresh(self):
        if self._t:
            f = self._t.function()
            self._t.cancel()
            self._t= Timer(self.timeout, f)
            self._t.start()

    def set_default(self):
        self._t and self._t.cancel()  # type: ignore
        object.__setattr__(self,"value", self.__default_value)

    def __setattr__(self, __name: str, __value: T):
        object.__setattr__(self,__name, __value)
        if __name == "value":
            _ = self._t and self._t.cancel()

            def callback_func():
                object.__setattr__(self,__name, self.__default_value)
                self._callback and self._callback()  # type: ignore
                self._t = self._start_time = None

            self._t = t = Timer(self.timeout, callback_func)
            t.start()
            self._start_time=time.time()


def chronos(value: T, timeout: float, *, callback: Optional[Callable] = None) -> ChronosItem[T]:
    return ChronosItem(value, timeout, callback)
