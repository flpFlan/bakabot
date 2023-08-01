"""依赖https://github.com/Infiniticity/akinator.py"""

# -- third party --
from third_party.akinator import CantGoBackAnyFurther
from third_party.akinator.async_aki import Akinator as Aki

# -- own --
from .base import Game, GameBehavior, register_to_game
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from accio import ACCIO
from utils import chronos, ChronosItem

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


graph: dict[int, ChronosItem] = {}


@register_to_game("akinator")
@register_to_game("Akinator")
class Akinator(Game):
    tick = 120

    async def __setup(self):
        if item := graph.get(self.owner_id):
            m = f"冷却中({600-item.elapsed_time:.0f}s)"
        else:
            graph[self.owner_id] = ChronosItem(self.owner_id, 600, lambda: graph.pop(self.owner_id))
            m = "tips:\n回复请使用(是|否|不知道|或许是|或许不是)\n退回上一问题请使用(/back)\n结束游戏请使用(/end)"
            await SendGroupMsg(self.group_id, m).do()
            self.aki = aki = Aki()
            if not (m := await aki.start_game("cn", child_mode=True)):
                m = f"啊哦Σ(⊙▽⊙，{ACCIO.bot.name}似乎发生了一些错误，请稍后重试。"
                self.kill()
        await SendGroupMsg(self.group_id, m).do()


class AkinatorBehavior(GameBehavior[Akinator]):
    interested = [GroupMessage]
    entrys = [r"^(?P<ans>是|不是|否|不知道|或许是|可能是|或许不是|可能不是|/back)$"]

    def check(self, evt: GroupMessage) -> bool:
        return evt.user_id == self.game.owner_id and self.filter(evt) is not None

    async def handle(self, evt: GroupMessage):
        if not (r := self.filter(evt)):
            return
        aki = self.game.aki
        ans = ch_to_en(r["ans"])
        if ans == "/back":
            try:
                m = await aki.back()
            except CantGoBackAnyFurther:
                m = "回退不能。"
        elif ans == "/end":
            self.game.kill()
            graph.pop(self.game.owner_id)
        else:
            m = await aki.answer(ans)

        if aki.progression and aki.progression > 80:
            await aki.win()
            self.game.kill()
            if guess := aki.first_guess:
                m = f"它应该是：{guess['name']} ({guess['description']})[CQ:image,file={guess['absolute_picture_path']}]"
            else:
                m = "我猜不出来了，你赢了。"
            await SendGroupMsg(self.game.group_id, m).do()
