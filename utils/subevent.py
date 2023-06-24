import asyncio
from collections import defaultdict
from typing import Callable, ClassVar


class SubEvent:
    registers: ClassVar[dict[str, set[Callable[[str, dict], None]]]] = defaultdict(set)

    @classmethod
    def emit(cls, sub_evt: str, payload: dict):
        _t = asyncio.gather(f(sub_evt, payload) for f in cls.registers[sub_evt])

    @classmethod
    def listen(cls, sub_evt: str, handler: Callable[[str, dict], None]):
        cls.registers[sub_evt].add(handler)

    @classmethod
    def unlisten(cls, sub_evt: str, handler: Callable[[str, dict], None]):
        cls.registers[sub_evt].remove(handler)
