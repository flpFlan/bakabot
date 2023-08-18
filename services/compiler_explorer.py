# -- stdlib --
import asyncio, re
from typing import ClassVar
from collections.abc import Iterable

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
            "c++": "g132",
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


doc = """
格式:
/run <lang>
[--compiler <compiler>]
[--args <args>]
[--u_args <u_args>]
[--lib <lib>]
[--input <input>]
<code>
参数:
    lang: 语言，可通过/lang查看
    compiler: 编译器，可通过/compiler <lang>查看
    args: 编译参数
    u_args: 用户参数
    lib: 链接库
    input: 输入
示例:
/run python --input Hello World!
print(input('echo: '))
""".strip()


class CompilerExplorer(Service):
    name = "Run Code"
    doc = doc


class CompilerExplorerCore(ServiceBehavior[CompilerExplorer], IMessageFilter):
    entrys = [r"^/run (?P<lang>\S+)(?P<params>(?:\s*^--\S+ .+$)+)?\s+(?P<code>[\s\S]*)"]
    entry_flags = re.MULTILINE

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

    def parse_args(self, args: Iterable) -> dict:
        rslt: dict = {
            "compiler": None,
            "args": [],
            "u_args": "",
            "lib": [],
            "input": None,
        }
        for arg in args:
            if arg.startswith("--compiler"):
                rslt["compiler"] = arg[11:]
            elif arg.startswith("--args"):
                rslt["args"].extend(arg[7:].split(" "))
            elif arg.startswith("--u_args"):
                rslt["u_args"] = arg[9:]
            elif arg.startswith("--lib"):
                rslt["lib"].extend(arg[6:].split(" "))
            elif arg.startswith("--input"):
                rslt["input"] += arg[8:] + "\n"
        return rslt

    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if not (r := self.filter(evt)):
            return

        lang, code = r["lang"].lower(), r["code"]
        if lang not in self.avilable_langs:
            m = "不支持这个语言"
        else:
            if params := r.group("params"):
                params = filter(None, map(lambda x: x.rstrip("\n"), params.split("--")))
            m = await self.compile(code, lang, **self.parse_args(params or []))
        await SendGroupMsg(evt.group_id, message=m).do()

    @OnEvent[GroupMessage].add_listener
    async def get_list(self, evt: GroupMessage):
        if evt.message.startswith("/lang"):
            m = ", ".join(self.avilable_langs.keys())
            await SendGroupMsg(evt.group_id, message=m).do()
        elif evt.message.startswith("/compiler"):
            lang = evt.message[9:].strip().lower()
            if lang not in self.avilable_langs:
                m = "不支持这个语言"
            else:
                m = ", ".join(self.avilable_langs[lang].compilers.avilable) or "None"
                if len(m) > 3666:
                    m = m[:1500] + " ..."
            await SendGroupMsg(evt.group_id, message=m).do()

    async def compile(
        self, code: str, lang: str, *, compiler, input, args, u_args, lib
    ):
        compiler = compiler or self.avilable_langs[lang].compilers.default
        if not compiler:
            return "没有指定编译器"
        if compiler not in self.avilable_langs[lang].compilers.avilable:
            return "没有这个编译器"
        form: dict = {
            "source": code,
            "compiler": compiler,
            "options": {
                "userArguments": u_args,
                "executeParameters": {
                    "args": args,
                    "stdin": input or None,
                },
                "compilerOptions": {"executorRequest": True},
                "filters": {"execute": True},
                "tools": [],
                "libraries": lib,
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
        rslt = ""
        if stdout := r.get("stdout"):
            rslt += "stdout:\n"
            for line in stdout:
                rslt += f'{line["text"]}\n'
            rslt += "\n"
        if stderr := r.get("stderr"):
            rslt += "stderr:\n"
            for line in stderr:
                rslt += f'{line["text"]}\n'
            rslt += "\n"
        if execTime := r.get("execTime"):
            rslt += f"execTime: {execTime}"
        return rslt.rstrip()
