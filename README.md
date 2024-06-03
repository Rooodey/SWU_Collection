# Star Wars Unlimited Collection Manager

## Overview
The Star Wars Unlimited Collection Manager is a web application designed to assist collectors of trading cards for the "Star Wars Unlimited" trading card game. It allows users to manage their card collection efficiently by providing features such as card price tracking, collection inventory management, and price trend analysis.

## Features
- **Card Database**: Utilizes an API to fetch card prices and populate the application's database.
- **Inventory Management**: Enables users to add cards to their collection, specifying details such as set, number, variant, foil status, and quantity.
- **Price Tracking**: Calculates the total value of the user's collection based on current card prices and tracks price trends over time.
- **Data Visualization**: Presents users with graphical representations of price trends for individual cards and the entire collection.

## Card Model
```python
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