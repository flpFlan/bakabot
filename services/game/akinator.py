"""依赖于https://github.com/Infiniticity/akinator.py"""

# -- stdlib --
from typing import cast

# -- third party --
from third_party.akinator import Akinator as Aki, CantGoBackAnyFurther

# -- own --
from .base import Game, GameBehavior, register_to_game
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg

# -- code --


def ch_to_en(ans: str):
    if ans == "是":
        return "yes"
    elif ans == "不是" or ans == "否":
        return "no"
    elif ans == "不知道":
        return "i"
    elif ans == "或许是" or ans == "可能是":
        return "p"
    elif ans == "或许不是" or ans == "可能不是":
        return "pn"
    else:
        return ans


class AkinatorBehavior(GameBehavior):
    interested = [GroupMessage]
    entrys = [r"^(?P<ans>是|不是|否|不知道|或许是|可能是|或许不是|可能不是|/back)$"]

    async def handle(self, evt: GroupMessage):
        game = cast(Akinator, self.game)
        if not evt.user_id == game.owner_id:
            return
        if not (r := self.filter(evt)):
            return
        aki = game.aki
        ans = ch_to_en(r.get("ans", ""))
        if ans == "/back":
            try:
                m = aki.back()
            except CantGoBackAnyFurther:
                m = "回退不能。"
        else:
            m = aki.answer(ans)
        if aki.progression > 80:  # type:ignore
            aki.win()
            game.kill()
            m = f"它应该是：{aki.first_guess['name']} ({aki.first_guess['description']})[CQ:image,file={aki.first_guess['absolute_picture_path']}]"  # type:ignore

        await SendGroupMsg(game.group_id, m).do(game.bot)  # type:ignore


@register_to_game("akinator")
@register_to_game("Akinator")
class Akinator(Game):
    tick = 120
    behavior = [AkinatorBehavior]

    async def start(self):
        m = "tips:\n回复请使用(是|否|不知道|或许是|或许不是)\n退回上一问题请使用(/back)"
        await SendGroupMsg(self.group_id, m).do()
        self.aki = aki = Aki()
        if not (m := aki.start_game("cn")):
            m = f"啊哦Σ(⊙▽⊙，{self.bot.name}似乎发生了一些错误，请稍后重试。"
            self.kill()
        await SendGroupMsg(self.group_id, m).do()
