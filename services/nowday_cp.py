# -- stdlib --
import random
from collections import defaultdict

# -- third party --
# -- own --
from services.base import IMessageFilter, Service, ServiceBehavior, OnEvent
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from cqhttp.api.group_info.GetGroupMemberList import GetGroupMemberList
from cqhttp.cqcode import At, Image
from accio import ACCIO
from utils.wrapper import Scheduled

# -- code --


class NowdayCP(Service):
    async def __setup(self):
        ACCIO.db.execute(
            "create table if not exists "
            "nowday_cp ("
            "group_id  integer, "
            "qq_number integer, "
            "cp_qq     integer, "
            "cp_name   text "
            ")"
        )
        self.cp_graph = self.get()

    def get(self) -> dict[int, dict[int, tuple[int, str]]]:
        ACCIO.db.execute("select group_id, qq_number, cp_qq, cp_name from nowday_cp")
        r = ACCIO.db.fatchall()
        graph = defaultdict(dict)
        for t in r:
            graph[t[0]][t[1]] = (t[2], t[3])

        return graph

    def add(self, group_id, qq_number, cp_qq, cp_name):
        ACCIO.db.execute(
            "insert into nowday_cp (group_id, qq_number, cp_qq, cp_name) values (?,?,?,?)",
            (group_id, qq_number, cp_qq, cp_name),
        )
        self.cp_graph[group_id][qq_number] = (cp_qq, cp_name)

    def delete(self, group_id, qq_number):
        if not group_id in self.cp_graph:
            return
        if not qq_number in self.cp_graph[group_id]:
            return
        ACCIO.db.execute(
            "delete from nowday_cp where group_id = ? and qq_number = ?",
            (group_id, qq_number),
        )
        self.cp_graph[group_id].pop(qq_number, None)

    def clear(self):
        ACCIO.db.execute("delete from nowday_cp")
        self.cp_graph.clear()


class NowdayCPCore(ServiceBehavior[NowdayCP]):
    async def __setup(self):
        Scheduled.Crontab().hour(0).add(self.refresh_cp)

    async def refresh_cp(self):
        self.service.clear()

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
            group_members = await GetGroupMemberList(group_id).do()
            assert group_members
            group_members = [
                (member["user_id"], member["card"] or member["nickname"])
                for member in group_members["data"]
            ]
            random.shuffle(group_members)
            member_graph = cp_graph[group_id]
            while True:
                cp_qq, cp_name = group_members.pop()
                if not cp_qq in member_graph and not cp_qq == 2854196310:  # Q群管家
                    break
            self.service.add(group_id, qq_number, cp_qq, cp_name)
            self.service.add(
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

    async def __setup(self):
        CPWord.instance = self
        ACCIO.db.execute(
            "create table if not exists "
            "cp_words  ("
            "qq_number integer primary key, "
            "word      text "
            ")"
        )
        self.words = self.get()

    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if not (r := self.filter(evt)):
            return
        word = r.get("word", "")
        if not len(word) > 200:
            self.set(evt.user_id, word)
            m = f"{At(evt.user_id)}\n设置成功~"
        else:
            m = "设置失败！字数溢出！"
        await SendGroupMsg(evt.group_id, m).do()

    def get(self) -> dict[int, str]:
        db = ACCIO.db
        db.execute("select qq_number, word from cp_words")
        r = db.fatchall()
        return {t[0]: t[1] for t in r}

    def set(self, qq_number, word):
        db = ACCIO.db
        db.execute(
            "insert or replace into cp_words (qq_number, word) values (?,?)",
            (qq_number, word),
        )
        self.words[qq_number] = word

    def delete(self, qq_number):
        if not qq_number in self.words:
            return
        db = ACCIO.db
        db.execute("delete from cp_words where qq_number = ?", (qq_number,))
        self.words.pop(qq_number, None)

    def clear(self):
        db = ACCIO.db
        db.execute("delete from cp_words")
        self.words.clear()
