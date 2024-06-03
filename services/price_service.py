from sqlalchemy import desc
from SWU_Collection.models import Session, LowestPrice, Avg7Days


class PriceService:

    def __init__(self):
        self.session = Session()

    def get_latest_avg_7_price(self, card):
        latest_avg_7_days_price = self.session.query(Avg7Days).filter(Avg7Days.card_id == card.id).order_by(
            desc(Avg7Days.date)).first()
        if latest_avg_7_days_price:
            return latest_avg_7_days_price.price
        return None

    def get_lowest_price(self, card):
        latest_lowest_price = self.session.query(LowestPrice).filter(LowestPrice.card_id == card.id).order_by(
            desc(LowestPrice.date)).first()
        if latest_lowest_price:
            return latest_lowest_price.price
        return None
