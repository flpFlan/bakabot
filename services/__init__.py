from .core.whitelist import WhiteList
from .core.blacklist import BlackList
from .core.message_pre_process import MessagePreProcess
from .core.command import Command
from .core.core_manager import CoreManager

from .baka_response import BakaResponse
from .message_failed_echo import MessageFailedEcho
from .search_song import SearchSong
from .yukkuri import Yukkuri
from .bilibili_cover import BilibiliCover
from .bilibili_ab_trans import BilibiliABTrans
from .random_touhou import RandomTouHou
from .random_art import RandomArt
from .search_image import SearchImage
from .nowday_news import NowdayNews
from .daxuexi_screenshot import DaXueXiScreenshot
from .pid import Pid
from .sponsor import Sponsor
from .emoji_mix import EmojiMix
from .nowday_news import NowdayNews
from .nowday_fortune import NowdayFortune
from .nowday_cp import NowdayCP
from .welcome_newcomer import WelcomeNewcomer
from .on_friend_group import OnFriendGroup
from .choose_or import ChooseOr
from .barber_shop import BarberShop
from .kfy import KFC
from .roll import Roll
from .poke_back import PokeBack
from .echo import Echo
from .take_back_msg import TakeBackMsg
from .compiler_explorer import CompilerExplorer
# from .thb_message_notify import THBMessageNotify

# from .game import *

# from importlib import import_module
# import os

# for i in os.listdir(os.path.dirname(__file__)):
#     if i.endswith(".py") and i != "__init__.py":
#         import_module(f".{i[:-3]}", __package__)
