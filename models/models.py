from sqlalchemy import Column, Integer, String, Boolean, JSON, ForeignKey, MetaData, Numeric, UniqueConstraint, \
    DateTime, DECIMAL, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class SWCards(Base):
    __tablename__ = "sw_cards"
    id = Column(Integer, primary_key=True, autoincrement=True)
    set = Column(String(10), nullable=False)
    number = Column(String(10), nullable=False)
    variant = Column(String, nullable=False)
    foil = Column(Boolean, nullable=False)
    name = Column(String, nullable=False)
    german_name = Column(String)
    subtitle = Column(String)
    german_subtitle = Column(String)
    rarity = Column(String(3), nullable=False)
    type = Column(String, nullable=False)
    card_url = Column(String(200))
    image_url = Column(String(200))
    amount = Column(Integer, default=0)
    lowest_price = relationship("LowestPrice", back_populates="card")
    price_trend = relationship("PriceTrend", back_populates="card")
    avg_1_day = relationship("Avg1Day", back_populates="card")
    avg_7_days = relationship("Avg7Days", back_populates="card")
    avg_30_days = relationship("Avg30Days", back_populates="card")
    __table_args__ = (UniqueConstraint('set', 'number', 'foil', name='uix_1'),)

    # @property
    # def aspects(self):
    #     return [aspect for aspect in self._aspects.split(';')]
    #
    # @aspects.setter
    # def aspects(self, value):
    #     self._aspects += f';{value}' if self._aspects else value


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

