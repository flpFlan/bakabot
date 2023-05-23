import asyncio
from typing import cast
from .base import Game, GameBehavior, register_to_game
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from cqhttp.api.group_operation.SetGroupAnonymousBan import SetGroupAnonymousBan
from cqhttp.api.group_operation.SetGroupBan import SetGroupBan


class RouletteBehavior(GameBehavior):
    interested = [GroupMessage]
    entrys = [r"^\*s$"]

    async def handle(self, evt: GroupMessage):
        if self.game.init_state:
            return
        game = cast(Roulette, self.game)
        if not evt.group_id == game.group_id:
            return
        if self.filter(evt) is None:
            return
        blt_nst = game.blt_nst
        import random

        if sum(blt_nst) == 0:  # all nst has blt
            if not random.choice(range(3)):
                await SendGroupMsg(evt.group_id, "玩家...子弹卡壳，发射不能∑(°口°๑)❢❢").do()
                return
        no_blt = random.choice(blt_nst)
        if not no_blt:
            await self.end_game(evt)
            game.kill()
        else:
            del blt_nst[-1]
            await SendGroupMsg(evt.group_id, "无事发生，有请下一位玩家。").do()

    async def end_game(self, evt: GroupMessage):
        bot = self.bot
        game = self.game
        group_id = evt.group_id
        if evt.anonymous:
            name = evt.anonymous.name
        else:
            name = evt.sender.card or evt.sender.nickname
        await SendGroupMsg(group_id, f"玩家{name}被弹幕击中满身疮痍，游戏结束").do()
        if game.set_ban:
            if evt.anonymous:
                await SetGroupAnonymousBan(
                    group_id, anonymous=evt.anonymous, duration=game.set_ban
                ).do()
            else:
                await SetGroupBan(group_id, evt.user_id, duration=game.set_ban).do()


class RouletteInit(GameBehavior):
    interested = [GroupMessage]
    entrys = [
        r"^\*s$",
        r"^设置(?P<action>弹巢数)(?P<arg>.+)",
        r"^设置(?P<action>子弹数)(?P<arg>.+)",
        r"^设置(?P<action>禁言)(?P<arg>.+)",
    ]

    async def handle(self, evt: GroupMessage):
        game = cast(Roulette, self.game)
        if not game.init_state:
            return
        if not evt.group_id == game.group_id:
            return
        if evt.message == "*s":
            game.init_state = False
            game.gen_blt_nst()
            return
        if r := self.filter(evt):
            action = r.get("action", "")
            arg = r.get("arg", "")
            if not arg.isdecimal():
                return evt
            arg = int(arg)
            if action == "弹巢数":
                if arg < game.blt_num:
                    return evt
                game.blt_nst_num = arg

            if action == "子弹数":
                if not 0 < arg <= game.blt_nst_num:
                    return evt
                game.blt_num = arg

            if action == "禁言":
                if arg < 0:
                    return evt
                game.set_ban = arg  # type: ignore
            await SendGroupMsg(evt.group_id, game.word).do()

    async def _callback(self, evt: GroupMessage):
        await SendGroupMsg(evt.group_id, "设置不能→_→").do()


@register_to_game("俄罗斯转盘")
@register_to_game("俄罗斯轮盘")
class Roulette(Game):
    behavior = [RouletteInit, RouletteBehavior]

    async def start(self):
        self.init_state = True
        self.blt_num = 1
        self.blt_nst_num = 6
        self.set_ban = False
        await SendGroupMsg(self.group_id, self.word).do()

    def gen_blt_nst(self):
        self.blt_nst = [0 for _ in range(self.blt_num)] + [1 for _ in range(self.blt_nst_num - self.blt_num)]
    @property
    def word(self):
        return f'现在进行初始化配置\n发送相关语句进行设置\n#设置弹巢数({self.blt_nst_num})\n#设置子弹数({self.blt_num})\n#设置禁言({self.set_ban or 0})(单位:秒)\n(需管理权限)\n键入"*s"以开始游戏。'
