from threading import Timer
from typing import Generic, TypeVar

T = TypeVar("T")


class ChronosItem(Generic[T]):
    def __init__(self, value: T, timeout: float):
        self.__default_value = value
        self.value = value
        self.timeout = timeout
        self.__t = None

    def refresh(self):
        if self.__t:
            f = self.__t.function()
            self.__t.cancel()
            self.__t = t = Timer(self.timeout, f)
            t.start()

    def set_default(self):
        _ = self.__t and self.__t.cancel()
        super().__setattr__("value", self.__default_value)

    def __setattr__(self, __name: str, __value: T):
        super().__setattr__(__name, __value)
        if __name == "value":
            _ = self.__t and self.__t.cancel()
            self.__t = t = Timer(
                self.timeout, lambda: super().__setattr__(__name, self.__default_value)
            )
            t.start()


def chronos(value: T, timeout: float) -> ChronosItem[T]:
    return ChronosItem(value, timeout)
