class Accio:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    # property
    @property
    def bot(self):
        from config import _Bot_

        return _Bot_

    @property
    def group_id(self):
        ...

    # method
    import asyncio
    from cqhttp.cqcode.cqcode import Image, Record

    def sgm(self, msg: str, group_id: int):
        ...

    def spm(self, msg, qq: int):
        ...

    def image(self, img: Image, group_id: int):
        ...

    def record(self, record: Record, group_id: int):
        ...

    def segm(self):
        ...

    def sfgm(self):
        ...


Accio = Accio()
