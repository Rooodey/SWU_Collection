from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .cards import SWCards
from .base import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
    card_quantities = relationship("CardQuantity", back_populates="user")


class CardQuantity(Base):
    __tablename__ = "card_quantity"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id))
    card_id = Column(Integer, ForeignKey(SWCards.id))
    quantity = Column(Integer)
    user = relationship("User", back_populates="card_quantities")
    card = relationship("SWCards", back_populates="quantities")
    __table_args__ = (UniqueConstraint('user_id', 'card_id', name='uix_2'),)
