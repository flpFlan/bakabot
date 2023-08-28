# -- stdlib --
# -- own --
from db.base import Model

# -- third party --
from sqlalchemy.orm import Mapped, mapped_column

# -- code --


class Service(Model):
    __tablename__ = "core_service"

    service: Mapped[str] = mapped_column(primary_key=True)
    service_on: Mapped[bool] = mapped_column(nullable=False, default=True)
