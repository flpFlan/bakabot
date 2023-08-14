import asyncio
from typing import Any, Callable, Coroutine


class CoreEvent:
    def __init__(self) -> None:
        self._event= asyncio.Event()
        self.subers: list[Callable[[], Coroutine]] = []

    def wait(self):
        return self._event.wait()

    async def invoke(self, **payload):
        self._event.set()
        if ts := [asyncio.create_task(f(**payload)) for f in self.subers]:
            await asyncio.wait(ts)
        await asyncio.sleep(0)
        self._event.clear()

    def subscribe(self, suber: Callable[[], Coroutine]):
        self.subers.append(suber)

    def unsubscribe(self, suber: Callable[[], Coroutine]):
        self.subers.remove(suber)

    def __iadd__(self, func:Callable[[], Coroutine]):
        self.subscribe(func)

    def __isub__(self, func:Callable[[], Coroutine]):
        self.unsubscribe(func)

    def __call__(self,**payload):
        return self.invoke(**payload)

