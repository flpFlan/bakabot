# -- stdlib --
import os
import random
from typing import cast

# -- third party --
from numpy.random import normal

# -- own --
from services.base import Service, ServiceBehavior, OnEvent
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from cqhttp.cqcode import At, Image
from accio import ACCIO
from utils.wrapper import Scheduled

# -- code --
exp = {"大吉": 96, "中吉": 80, "小吉": 64, "小凶": 48, "中凶": 32, "大凶": 16, "baka": 999}


class NowdayFortune(Service):
    name = "今日运势"

    async def __setup(self):
        await ACCIO.db.execute(
            "create table if not exists "
            "nowday_fortune ("
            "qq_number      integer primary key, "
            "fortune        text, "
            "money          integer, "
            "love           integer, "
            "work           integer "
            ")"
        )
        self.fortune_graph = await self.get()

    async def get(self) -> dict[int, list[int | str]]:
        await ACCIO.db.execute("select qq_number,fortune,money,love,work from nowday_fortune")
        r = await ACCIO.db.fatchall()

        return {l[0]: [l[1], l[2], l[3]] for l in r}

    async def add(self, qq_number, fortune, money, love, work):
        await ACCIO.db.execute(
            "insert or replace into nowday_fortune (qq_number,fortune,money,love,work) values (?,?,?,?,?)",
            (qq_number, fortune, money, love, work),
        )
        self.fortune_graph[qq_number] = [fortune, money, love, work]

    async def delete(self, qq_number):
        if not qq_number in self.fortune_graph:
            return
        await ACCIO.db.execute("delete from nowday_fortune where qq_number = ?", (qq_number,))
        self.fortune_graph.pop(qq_number, None)

    async def clear(self):
        await ACCIO.db.execute("delete from nowday_fortune")
        self.fortune_graph.clear()


class NowdayFortuneCore(ServiceBehavior[NowdayFortune]):
    async def __setup(self):
        with Scheduled.Crontab(self.service) as schedule:
            schedule.hour(0).add(self.refresh_fortune)

    async def refresh_fortune(self):
        self.service.clear

    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if not evt.message in ("jrys", "今日运势", "每日运势"):
            return
        qq_number = evt.user_id

        if qq_number in self.service.fortune_graph:
            m = f'{At(qq_number)}\n命运的轨迹在一次日月轮换之内只能窥探一次，请明天再来吧(/"≡ _ ≡)='
            await SendGroupMsg(evt.group_id, m).do()
            return

        if random.getrandbits == 0:  # bonus
            m = "今日运势\nbakabakabakabaka，bakabaka，bakabakabakabakabakabaka，baka！(｀∀´)Ψ "
            await SendGroupMsg(evt.group_id, m).do()
            return

        if random.getrandbits == 0:  # another bonus
            await self.service.add(qq_number, "baka", 999, 999, 999)
            m = "今日运…∑(°口°๑)❢❢少年，你的命我看不透啊…莫非你就是传说中的主角？去开拓属于自己的命运吧！我命由我不由天(｡ì _ í｡)"
            await SendGroupMsg(evt.group_id, m).do()
            return

        fortune = random.choice(["大吉", "中吉", "小吉", "小凶", "中凶", "大凶"])
        money = int(normal(exp[fortune], 20))
        love = int(normal(exp[fortune], 20))
        work = int(normal(exp[fortune], 20))
        await self.service.add(qq_number, fortune, money, love, work)

        path = os.path.abspath(f"src/fortune/{fortune}.png")
        m = f"{At(qq_number)}\n运势：{fortune}\n爱情运：{love}\n财运：{money}\n事业运：{work}{Image(f'file:///{path}')}"

        await SendGroupMsg(evt.group_id, m).do()
