# -- stdlib --
import random
from collections import defaultdict
from typing import ClassVar, Self

# -- third party --
from sqlalchemy import select, delete

# -- own --
from services.base import IMessageFilter, Service, ServiceBehavior, OnEvent
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from cqhttp.api.group_info.GetGroupMemberList import GetGroupMemberList
from cqhttp.cqcode import At, Image
from accio import ACCIO
from utils.wrapper import Scheduled
from db.models.service import NowdayCP as NowdayCPModel, CPWord as CPWordModel

# -- code --

doc = """
格式:
    jrcp
    今日cp
    /cp <text>
用例:
    /cp 今天好高兴啊
""".strip()


class NowdayCP(Service):
    name = "今日CP"
    doc = doc

    async def __setup(self):
        self.cp_graph = await self.get()

    async def get(self) -> dict[int, dict[int, tuple[int, str]]]:
        graph: defaultdict[int, dict[int, tuple[int, str]]] = defaultdict(dict)
        session = ACCIO.db.session
        async with session.begin():
            rslt = (await session.scalars(select(NowdayCPModel))).all()
            for t in rslt:
                graph[t.group_id][t.qq_number] = (t.cp_qq, t.cp_name)

        return graph

    async def add(self, group_id, qq_number, cp_qq, cp_name):
        session = ACCIO.db.session
        async with session.begin():
            session.add(
                NowdayCPModel(
                    group_id=group_id, qq_number=qq_number, cp_qq=cp_qq, cp_name=cp_name
                )
            )
        self.cp_graph[group_id][qq_number] = (cp_qq, cp_name)

    async def delete(self, group_id, qq_number):
        if not group_id in self.cp_graph:
            return
        if not qq_number in self.cp_graph[group_id]:
            return
        session = ACCIO.db.session
        async with session.begin():
            await session.execute(
                delete(NowdayCPModel).where(
                    NowdayCPModel.qq_number == qq_number
                    and NowdayCPModel.group_id == group_id
                )
            )

        self.cp_graph[group_id].pop(qq_number, None)

    async def clear(self):
        session = ACCIO.db.session
        async with session.begin():
            await session.execute(delete(NowdayCPModel))
        self.cp_graph.clear()


class NowdayCPCore(ServiceBehavior[NowdayCP]):
    async def __setup(self):
        with Scheduled.Crontab(self.service) as schedule:
            schedule.hour(0).add(self.refresh_cp)

    async def refresh_cp(self):
        await self.service.clear()

    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if not evt.message in ("jrcp", "今日cp", "今日CP"):
            return
        cp_graph = self.service.cp_graph
        group_id = evt.group_id
        qq_number = evt.user_id

        if cp := cp_graph[group_id].get(qq_number, None):
            cp_qq = cp[0]
            cp_name = cp[1]
        else:
            resp = await GetGroupMemberList(group_id).do()
            group_members = [
                (member["user_id"], member["card"] or member["nickname"])
                for member in resp["data"]
            ]
            random.shuffle(group_members)
            member_graph = cp_graph[group_id]
            while True:
                cp_qq, cp_name = group_members.pop()
                if not cp_qq in member_graph and not cp_qq == 2854196310:  # Q群管家
                    break
            await self.service.add(group_id, qq_number, cp_qq, cp_name)
            await self.service.add(
                group_id, cp_qq, qq_number, evt.sender.card or evt.sender.nickname
            )
        photo = f"http://q1.qlogo.cn/g?b=qq&nk={cp_qq}&s=640"
        if word := CPWord.instance.words.get(cp_qq, None):
            m = f"{At(qq_number)}\n您的今日cp是:\n{cp_name}{Image(photo)}\n>>>\n{word}"
        else:
            m = f"{At(qq_number)}\n您的今日cp是:\n{cp_name}{Image(photo)}"

        await SendGroupMsg(group_id, m).do()


class CPWord(ServiceBehavior[NowdayCP], IMessageFilter):
    entrys = [r"^/cp\s(?P<word>.+)"]
    instance: ClassVar[Self]

    async def __setup(self):
        CPWord.instance = self
        self.words = await self.get()

    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if not (r := self.filter(evt)):
            return
        word = r.group("word")
        if not len(word) > 200:
            await self.set(evt.user_id, word)
            m = f"{At(evt.user_id)}\n设置成功~"
        else:
            m = "设置失败！字数溢出！"
        await SendGroupMsg(evt.group_id, m).do()

    async def get(self) -> dict[int, str]:
        session = ACCIO.db.session
        async with session.begin():
            rslt = (await session.scalars(select(CPWordModel))).all()
            return {int(t.qq_number): str(t.word) for t in rslt}

    async def set(self, qq_number, word):
        session = ACCIO.db.session
        async with session.begin():
            await session.merge(NowdayCPModel(qq_number=qq_number, word=word))
        self.words[qq_number] = word

    async def delete(self, qq_number):
        if not qq_number in self.words:
            return
        session = ACCIO.db.session
        async with session.begin():
            await session.execute(
                delete(NowdayCPModel).where(NowdayCPModel.qq_number == qq_number)
            )
        self.words.pop(qq_number, None)

    async def clear(self):
        await ACCIO.db.session.execute(delete(NowdayCPModel))
        await ACCIO.db.session.commit()
        self.words.clear()
