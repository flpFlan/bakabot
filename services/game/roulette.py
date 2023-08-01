from .base import Game, GameBehavior, register_to_game
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from cqhttp.api.group_operation.SetGroupAnonymousBan import SetGroupAnonymousBan
from cqhttp.api.group_operation.SetGroupBan import SetGroupBan


@register_to_game("俄罗斯转盘")
@register_to_game("俄罗斯轮盘")
class Roulette(Game):
    async def __setup(self):
        self.init_state = True
        self.blt_num = 1
        self.blt_nst_num = 6
        self.set_ban = False
        self.ban_duration = 0
        await SendGroupMsg(self.group_id, self.word).do()

    def gen_blt_nst(self):
        self.blt_nst = [0 for _ in range(self.blt_num)] + [
            1 for _ in range(self.blt_nst_num - self.blt_num)
        ]

    @property
    def word(self):
        return f'现在进行初始化配置\n发送相关语句进行设置\n#设置弹巢数({self.blt_nst_num})\n#设置子弹数({self.blt_num})\n#设置禁言({self.set_ban and self.ban_duration})(单位:秒)\n(需管理权限)\n键入"*s"以开始游戏。'


class RouletteInit(GameBehavior[Roulette]):
    interested = [GroupMessage]
    entrys = [
        r"^\*s$",
        r"^设置(?P<action>弹巢数)(?P<arg>.+)",
        r"^设置(?P<action>子弹数)(?P<arg>.+)",
        r"^设置(?P<action>禁言)(?P<arg>.+)",
    ]

    def check(self, evt: GroupMessage) -> bool:
        return self.game.init_state and evt.group_id == self.game.group_id and self.filter(evt) is not None

    async def handle(self, evt: GroupMessage):
        game = self.game
        if evt.message == "*s":
            game.init_state = False
            game.gen_blt_nst()
            return
        if r := self.filter(evt):
            action = r["action"]
            arg = r["arg"]
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
                game.set_ban = bool(arg)
                game.ban_duration = arg
            await SendGroupMsg(evt.group_id, game.word).do()

    async def _callback(self, evt: GroupMessage):
        await SendGroupMsg(evt.group_id, "设置不能→_→").do()


class RouletteBehavior(GameBehavior[Roulette]):
    interested = [GroupMessage]

    def check(self, evt: GroupMessage) -> bool:
        return not self.game.init_state and evt.group_id == self.game.group_id and evt.message == "*s"

    async def handle(self, evt: GroupMessage):
        blt_nst = self.game.blt_nst
        import random

        if sum(blt_nst) == 0:  # all nst has blt
            if not random.choice(range(3)):
                await SendGroupMsg(evt.group_id, "玩家...子弹卡壳，发射不能∑(°口°๑)❢❢").do()
                return
        no_blt = random.choice(blt_nst)
        if not no_blt:
            await self.end_game(evt)
            self.game.kill()
        else:
            del blt_nst[-1]
            await SendGroupMsg(evt.group_id, "无事发生，有请下一位玩家。").do()

    async def end_game(self, evt: GroupMessage):
        group_id = evt.group_id
        if evt.anonymous:
            name = evt.anonymous.name
        else:
            name = evt.sender.card or evt.sender.nickname
        await SendGroupMsg(group_id, f"玩家{name}被弹幕击中满身疮痍，游戏结束").do()
        if duration := self.game.ban_duration:
            if evt.anonymous:
                await SetGroupAnonymousBan(
                    group_id, anonymous=evt.anonymous, duration=duration
                ).do()
            else:
                await SetGroupBan(group_id, evt.user_id, duration=duration).do()
