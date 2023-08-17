# -- stdlib --
import re
from typing import cast

# -- third party --
import emoji

# -- own --
from services.base import IMessageFilter, Service, ServiceBehavior, OnEvent
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg
from utils.request import Request
from cqhttp.cqcode import Image


# -- code --
emojis = sorted(emoji.EMOJI_DATA, key=len, reverse=True)
pattern = "(" + "|".join(re.escape(u) for u in emojis) + ")"


class EmojiMix(Service):
    pass


class EmojiError(Exception):
    pass


class EmojiMixCore(ServiceBehavior[EmojiMix], IMessageFilter):
    entrys = [rf"^emoji合成\s*(?P<emoji>{pattern}{{2}})$"]

    @OnEvent[GroupMessage].add_listener
    async def handle(self, evt: GroupMessage):
        if not (r := self.filter(evt)):
            return
        emoji1, emoji2 = cast(tuple[str, str], r.group("emoji"))
        self.format_emoji(emoji1)
        self.format_emoji(emoji2)
        try:
            url = await self.get_mix_url(emoji1, emoji2)
            m = f"{Image(file=url)}"
        except EmojiError:
            m = '啊哦，似乎发生了一些错误Σ(⊙▽⊙"a\n请检查内容后重试'

        await SendGroupMsg(evt.group_id, m).do()

    async def get_mix_url(self, emoji1, emoji2):
        emoji1 = hex(ord(emoji1)).replace("0x", "u")
        emoji2 = hex(ord(emoji2)).replace("0x", "u")

        for _ in range(2):
            url = f"https://www.gstatic.com/android/keyboard/emojikitchen/20201001/{emoji1}/{emoji1}_{emoji2}.png"
            if (await Request.get(url)).ok:
                return url
            emoji1, emoji2 = emoji2, emoji1

        raise EmojiError()

    def format_emoji(self, emoji: str):
        if "️" in emoji:
            emoji = emoji.replace("️", "") + "-ufe0f"
        return emoji
