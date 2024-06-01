from sqlalchemy import Column, Integer, Boolean, Date, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from .base import Base
from .cards import SWCards

class LowestPrice(Base):
    __tablename__ = "lowest_price"
    id = Column(Integer, primary_key=True, autoincrement=True)
    card_id = Column(Integer, ForeignKey(SWCards.id), nullable=False)
    card = relationship("SWCards", back_populates="lowest_price")
    date = Column(Date, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)


class PriceTrend(Base):
    __tablename__ = "price_trend"
    id = Column(Integer, primary_key=True, autoincrement=True)
    card_id = Column(Integer, ForeignKey(SWCards.id), nullable=False)
    card = relationship("SWCards", back_populates="price_trend")
    date = Column(Date, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)


class Avg1Day(Base):
    __tablename__ = "avg_1_day"
    id = Column(Integer, primary_key=True, autoincrement=True)
    card_id = Column(Integer, ForeignKey(SWCards.id), nullable=False)
    card = relationship("SWCards", back_populates="avg_1_day")
    date = Column(Date, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)


class Avg7Days(Base):
    __tablename__ = "avg_7_day"
    id = Column(Integer, primary_key=True, autoincrement=True)
    card_id = Column(Integer, ForeignKey(SWCards.id), nullable=False)
    card = relationship("SWCards", back_populates="avg_7_days")
    date = Column(Date, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)


class Avg30Days(Base):
    __tablename__ = "avg_30_day"
    id = Column(Integer, primary_key=True, autoincrement=True)
    card_id = Column(Integer, ForeignKey(SWCards.id), nullable=False)
    card = relationship("SWCards", back_populates="avg_30_days")
    date = Column(Date, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)

class UpdateStatus(Base):
    __tablename__ = "update_status"
    date = Column(Date, primary_key=True)
    finished = Column(Boolean, default=False)
    last_id = Column(Integer, nullable=False)
