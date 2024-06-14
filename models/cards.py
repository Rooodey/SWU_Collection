from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base

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
    quantities = relationship("CardQuantity", back_populates="card")
    lowest_price = relationship("LowestPrice", back_populates="card")
    price_trend = relationship("PriceTrend", back_populates="card")
    avg_1_day = relationship("Avg1Day", back_populates="card")
    avg_7_days = relationship("Avg7Days", back_populates="card")
    avg_30_days = relationship("Avg30Days", back_populates="card")
    __table_args__ = (UniqueConstraint('set', 'number', 'foil', name='uix_1'),)
