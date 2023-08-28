# -- stdlib --
# -- own --
from db.base import Model

# -- third party --
from sqlalchemy.orm import Mapped, mapped_column


class BlackList(Model):
    __tablename__ = "service_blacklist"

    qq_number: Mapped[int] = mapped_column(primary_key=True)


class BlockGroup(Model):
    __tablename__ = "service_blockgroup"

    group_id: Mapped[int] = mapped_column(primary_key=True)


class WhiteList(Model):
    __tablename__ = "service_whitelist"

    group_id: Mapped[int] = mapped_column(primary_key=True)


class NowdayCP(Model):
    __tablename__ = "service_nowdaycp"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(nullable=False)
    qq_number: Mapped[int] = mapped_column(nullable=False)
    cp_qq: Mapped[int] = mapped_column(nullable=False)
    cp_name: Mapped[str] = mapped_column(nullable=False)


class CPWord(Model):
    __tablename__ = "service_nowdaycp_word"

    qq_number: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str] = mapped_column(nullable=True, default="")


class NowdayFortune(Model):
    __tablename__ = "service_nowdayfortune"

    qq_number: Mapped[int] = mapped_column(primary_key=True)
    fortune: Mapped[str] = mapped_column(nullable=False)
    money: Mapped[int] = mapped_column(nullable=False)
    love: Mapped[int] = mapped_column(nullable=False)
    work: Mapped[int] = mapped_column(nullable=False)


class NotifyGroup(Model):
    __tablename__ = "service_thbmessagenotify"

    group_id: Mapped[int] = mapped_column(primary_key=True)
