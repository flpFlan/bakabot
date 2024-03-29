# -- third party --
from akinator import CantGoBackAnyFurther, AkiTimedOut
from akinator.async_aki import Akinator as Aki
from aiohttp import ClientSession, TCPConnector
from typing_extensions import override

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
CONN=TCPConnector(verify_ssl=False)
COOL_DOWN_SEC=300


@register_to_game("akinator")
@register_to_game("Akinator")
class Akinator(Game):
    tick = 120

    async def __setup(self):
        if item := graph.get(self.owner_id):
            remain_time = COOL_DOWN_SEC-item.elapsed_time
            if remain_time > 0:
                await SendGroupMsg(self.group_id, f"冷却中({remain_time:.0f}s)").do()
                self.kill()
                return
            else:
                if _t:=graph[self.owner_id]._t:
                    _t.cancel()
                del graph[self.owner_id]
        graph[self.owner_id] = ChronosItem(self.owner_id, COOL_DOWN_SEC, lambda: graph.pop(self.owner_id))
        graph[self.owner_id].value = self.owner_id # for start countdown

        m = "tips:\n回复请使用(是|否|不知道|或许是|或许不是)\n退回上一问题请使用(/back)\n结束游戏请使用(/end)"
        await SendGroupMsg(self.group_id, m).do()
        self.aki = aki = Aki()
        if not (m := await aki.start_game("cn", child_mode=True,client_session=ClientSession(trust_env=True,connector=CONN))):
            m = f"啊哦Σ(⊙▽⊙，{ACCIO.bot.name}似乎发生了一些错误，请稍后重试。"
            self.kill()

        await SendGroupMsg(self.group_id, m).do()


class AkinatorBehavior(GameBehavior[Akinator, GroupMessage]):
    entrys = [r"^(?P<ans>是|不是|否|不知道|或许是|可能是|或许不是|可能不是|/back|/end)$"]

    @override
    def check(self, evt: GroupMessage) -> bool:
        return (evt.user_id == self.game.owner_id) and self.filter(evt) is not None

    @override
    async def handle(self, evt: GroupMessage):
        if not (r := self.filter(evt)):
            return
        aki = self.game.aki
        ans = ch_to_en(r["ans"])
        if ans == "/back":
            try:
                m = await aki.back() or "No Answer"
            except CantGoBackAnyFurther:
                m = "回退不能。"
        elif ans == "/end":
            self.game.kill()
            graph.pop(self.game.owner_id)
            m = f"游戏结束({self.game.owner_id})"

        elif aki.progression and aki.progression > 80:
            await aki.win()
            self.game.kill()
            if guess := aki.first_guess:
                m = f"它应该是：{guess['name']} ({guess['description']})[CQ:image,file={guess['absolute_picture_path']}]"
            else:
                m = "我猜不出来了，你赢了。"
        else:
            try:
                m = await aki.answer(ans) or "No Answer"
            except AkiTimedOut:
                m = f"游戏超时。({self.game.owner_id})"
                self.game.kill()
            except:
                m="网络错误."

        await SendGroupMsg(self.game.group_id, m).do()
