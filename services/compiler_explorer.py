# -- stdlib --
import asyncio
from typing import ClassVar

# -- third party --
# -- own --
from services.base import Service, ServiceBehavior, IMessageFilter, OnEvent
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.request import Request


# -- code --
OptStr = str | None


class Language:
    class Compilers:
        _default_compiler: ClassVar[dict[str, str]] = {
            "assembly": "nasm21402",
            "csharp": "dotnet707csharp",
            "c": "cg132",
            "cpp": "g132",
            "go": "gl1200",
            "java": "java2000",
            "python": "python311",
            "javascript": "v8trunk",
            "rust": "r1710",
            "typescript": "tsc_0_0_35_gc",
        }

        @classmethod
        def default_of(cls, lang: str) -> OptStr:
            return cls._default_compiler.get(lang)

        def __init__(self):
            self.avilable = []
            self.default: OptStr = None

    def __init__(self, id: str):
        self.id = id
        self.compilers = self.__class__.Compilers()


class CompilerExplorer(Service):
    pass


class CompilerExplorerCore(ServiceBehavior[CompilerExplorer], IMessageFilter):
    entrys = [r"^/run (?P<lang>.+)\s+(?P<code>.*)"]

    async def __setup(self):
        headers = {"Accept": "application/json"}
        r = await Request[list].get_json(
            "https://gcc.godbolt.org/api/languages", headers=headers
        )
        self.avilable_langs = dict(map(lambda x: (x["id"], Language(x["id"])), r))

        async def task():
            for lang in self.avilable_langs:
                r = await Request[list].get_json(
                    f"https://gcc.godbolt.org/api/compilers/{lang}", headers=headers
                )
                self.avilable_langs[lang].compilers.avilable = list(
                    map(lambda x: x["id"], r)
                )
                if default := Language.Compilers.default_of(lang):
                    self.avilable_langs[lang].compilers.default = default

                await asyncio.sleep(1)

        asyncio.create_task(task())

    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if not (r := self.filter(evt)):
            return

        lang, code = r["lang"].lower(), r["code"]
        if lang not in self.avilable_langs:
            m = "不支持这个语言"
        else:
            m = await self.compile(code, lang)
        await SendGroupMsg(evt.group_id, message=m).do()

    async def compile(
        self, code: str, lang: str, *, compiler: OptStr = None, input: str = ""
    ):
        compiler = compiler or self.avilable_langs[lang].compilers.default
        if not compiler:
            return "没有指定编译器"
        if compiler not in self.avilable_langs[lang].compilers.avilable:
            return "没有这个编译器"
        form = {
            "source": code,
            "compiler": compiler,
            "options": {
                "userArguments": "-O3",
                "executeParameters": {
                    "args": "",
                    "stdin": input,
                },
                "compilerOptions": {"executorRequest": True},
                "filters": {"execute": True},
                "tools": [],
                "libraries": [],
            },
            "lang": lang,
            "allowStoreCodeDebug": True,
        }

        headers = {"Accept": "application/json"}
        r = await Request[dict].post_json(
            f"https://gcc.godbolt.org/api/compiler/{compiler}/compile",
            headers=headers,
            json=form,
        )

        rslt = "stdout:\n"
        for line in r["stdout"]:
            rslt += f'{line["text"]}\n'
        rslt += "stderr:\n"
        for line in r["stderr"]:
            rslt += f'{line["text"]}\n'
        rslt += f"execTime: {r['execTime']}"
        return rslt
