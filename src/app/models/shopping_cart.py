from inspect import cleandoc

from sqlalchemy import CheckConstraint, Column, Integer, BigInteger, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from telegram import InlineKeyboardButton

from core.database import Base
from .user import User
from .catalog import Catalog


class ShoppingCart(Base):
    __tablename__ = "shopping_cart"

    catalog_id = Column(Integer, ForeignKey("catalog.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(BigInteger, ForeignKey("user.tg_id", ondelete="CASCADE"), primary_key=True)
    count = Column(Integer, CheckConstraint('count >= 1', name='check_count'), nullable=False)

    catalog: Mapped["Catalog"] = relationship(lazy="selectin")
    user: Mapped["User"] = relationship(
        back_populates="shopping_carts", lazy="selectin"
    )
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def to_text(self):
        return cleandoc(
            f"""
            *Позиция* - `{self.catalog_id}`;
            *Имя позиции* - `{self.catalog.name}`;
            *Описание позиции* - `{self.catalog.description}`;
            *Количество в корзине* - `{self.count}`;
            *Всего доступно* - `{len(self.catalog.products)}`;
            """
        )

    def to_button(self, offset: int, limit: int, return_to: str = "main"):
        return [
            InlineKeyboardButton(
                text=f"{self.catalog.name}; \n{self.catalog.description}",
                callback_data=f"solo_shopping_cart:{self.catalog_id}:{offset}:{limit};{return_to}",
            )
        ]

