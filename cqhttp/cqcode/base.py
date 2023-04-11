import re


class CQCode:
    cq: str

    @classmethod
    def select_from(cls, msg: str):
        pattern = re.compile(rf"\[CQ:(?P<CQ>{cls.cq})(?P<data>.+=.+*)\]")
        return cls()


all_cqcodes = {}


def register_to_cqcodes(cls):
    cq = cls.cq
    assert cq not in all_cqcodes
    all_cqcodes[cq] = cls

    return cls
