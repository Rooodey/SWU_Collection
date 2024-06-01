from .base import Base, engine, Session
from .cards import SWCards
from .prices import LowestPrice, PriceTrend, Avg1Day, Avg7Days, Avg30Days, UpdateStatus

__all__ = ["Base", "engine", "Session", "SWCards", "LowestPrice", "PriceTrend", "Avg1Day", "Avg7Days", "Avg30Days", "UpdateStatus"]

def init_db():
    Base.metadata.create_all(engine)