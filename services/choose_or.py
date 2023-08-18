# -- stdlib --
import random

# -- third party --
# -- own --
from services.base import Service, ServiceBehavior, IMessageFilter, OnEvent
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from cqhttp.cqcode import At

# -- code --

doc = """
描述:
    帮你做选择
格式:
    选择<选项1>还是<选项2>[还是<选项3>...]
用例:
    选择1还是2
""".strip()


class ChooseOr(Service):
    doc = doc


class ChooseOrCore(ServiceBehavior[ChooseOr], IMessageFilter):
    entrys = [r"^选择(?P<choices>.+还是.+)"]

    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if not (r := self.filter(evt)):
            return
        choices = r.group("choices").split("还是")
        if not all(choices):
            return
        final_choice = random.choice(choices)
        m = f"{At(evt.user_id)}\n"
        for i, c in enumerate(choices):
            m += f"{i + 1}、{c}\n"
        m += f"建议你选择：{final_choice}"

        SendGroupMsg(evt.group_id, m).forget()
