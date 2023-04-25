# -- stdlib --
import os
import random
from typing import cast
from collections import defaultdict

# -- third party --
# -- own --
from services.base import (
    IMessageFilter,
    register_to,
    Service,
    EventHandler,
    SheduledHandler,
)
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from cqhttp.api.group_info.GetGroupMemberList import GetGroupMemberList

# -- code --


class NowdayCPCore(EventHandler):
    interested = [GroupMessage]

    async def handle(self, evt: GroupMessage):
        if not evt.message in ("jrcp", "今日cp", "今日CP"):
            return
        service = cast(NowdayCP, self.service)
        cp_graph = service.cp_graph
        bot = self.bot
        group_id = evt.group_id
        qq_number = evt.user_id

        if cp := cp_graph[group_id].get(qq_number, None):
            cp_qq = cp[0]
            cp_name = cp[1]
        else:
            group_members = await GetGroupMemberList(group_id).do(bot)
            assert group_members
            group_members = [
                (member.user_id, member.card or member.nickname)
                for member in group_members.data
            ]
            random.shuffle(group_members)
            member_graph = cp_graph[group_id]
            while True:
                cp = group_members.pop()
                if not cp[0] in member_graph:
                    if not cp[0] == 2854196310 or len(member_graph) == 0:
                        cp_qq, cp_name = cp
                        break
            service.add(group_id, qq_number, cp_qq, cp_name)
        photo = f"http://q1.qlogo.cn/g?b=qq&nk={cp_qq}&s=640"
        if word := CPWord.instance.words.get(qq_number, None):
            m = f"[CQ:at,qq={qq_number}]\n您的今日cp是:\n{cp_name}[CQ:image,file={photo}]\n>>>\n{word}"
        else:
            m = f"[CQ:at,qq={qq_number}]\n您的今日cp是:\n{cp_name}[CQ:image,file={photo}]"

        await SendGroupMsg(group_id, m).do(bot)


class RefreshCP(SheduledHandler):
    shedule_trigger = "cron"
    args = {"hour": 0, "minute": 0, "second": 0}

    async def handle(self):
        service = cast(NowdayCP, self.service)
        service.clear()


class CPWord(EventHandler, IMessageFilter):
    interested = [GroupMessage]
    entrys = [r"^/cp\s(?P<word>.+)"]

    def __init__(self, service):
        super().__init__(service)
        CPWord.instance = self

    def run(self):
        super().run()
        bot = self.bot
        bot.db.execute(
            "create table if not exists "
            "cp_words  ("
            "qq_number integer primary key, "
            "word      text "
            ")"
        )
        self.words = self.get()

    async def handle(self, evt: GroupMessage):
        if not (r := self.filter(evt)):
            return
        word = r.get("word", "")
        if not len(word) > 200:
            self.set(evt.user_id, word)
            m = f"[CQ:at,qq={evt.user_id}]\n设置成功~"
        else:
            m = "设置失败！字数溢出！"
        await SendGroupMsg(evt.group_id, m).do(self.bot)

    def get(self) -> dict[int, str]:
        db = self.bot.db
        db.execute("select qq_number, word from cp_words")
        r = db.fatchall()
        return {t[0]: t[1] for t in r}

    def set(self, qq_number, word):
        db = self.bot.db
        db.execute(
            "insert or replace into cp_words (qq_number, word) values (?,?)",
            (qq_number, word),
        )
        self.words[qq_number] = word

    def delete(self, qq_number):
        if not qq_number in self.words:
            return
        db = self.bot.db
        db.execute("delete from cp_words where qq_number = ?", (qq_number,))
        self.words.pop(qq_number, None)

    def clear(self):
        db = self.bot.db
        db.execute("truncate cp_words")
        self.words.clear()


@register_to("ALL")
class NowdayCP(Service):
    cores = [NowdayCPCore, RefreshCP, CPWord]

    async def start(self):
        await super().start()
        bot = self.bot
        bot.db.execute(
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
        db = self.bot.db
        db.execute("select group_id, qq_number, cp_qq, cp_name from nowday_cp")
        r = db.fatchall()
        graph = defaultdict(dict)
        for t in r:
            graph[t[0]][t[1]] = (t[2], t[3])

        return graph

    def add(self, group_id, qq_number, cp_qq, cp_name):
        db = self.bot.db
        db.execute(
            "insert into nowday_cp (group_id, qq_number, cp_qq, cp_name) values (?,?,?,?)",
            (group_id, qq_number, cp_qq, cp_name),
        )
        self.cp_graph[group_id][qq_number] = (cp_qq, cp_name)

    def delete(self, group_id, qq_number):
        if not group_id in self.cp_graph:
            return
        if not qq_number in self.cp_graph[group_id]:
            return
        db = self.bot.db
        db.execute(
            "delete from nowday_cp where group_id = ? and qq_number = ?",
            (group_id, qq_number),
        )
        self.cp_graph[group_id].pop(qq_number, None)

    def clear(self):
        db = self.bot.db
        db.execute("truncate nowday_cp")
        self.cp_graph.clear()
