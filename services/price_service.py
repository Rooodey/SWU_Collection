from datetime import date
from sqlalchemy import desc
from SWU_Collection.models import Session, SWCards, LowestPrice, PriceTrend, Avg1Day, Avg7Days, Avg30Days, UpdateStatus
from SWU_Collection.crawler import get_price_from_url


class PriceService:

    def __init__(self):
        self.session = Session()

    def set_new_prices(self):
        sw_cards = self.session.query(SWCards).all()
        today = date.today()
        status = self.session.query(UpdateStatus).filter_by(date=today).first()
        last_id = 0
        if status:
            if status.finished:
                return True
            else:
                last_id = status.last_id
        else:
            status = UpdateStatus(date=today, last_id=0)
            self.session.add(status)
            self.session.commit()
            self.session.refresh(status)
        try:
            for card in sw_cards:
                if card.id <= last_id:
                    continue
                url = card.card_url
                all_prices = get_price_from_url(url)
                new_lowest_price = LowestPrice(date=today, price=all_prices["lo_price"])
                card.lowest_price.append(new_lowest_price)
                new_price_trend = PriceTrend(date=today, price=all_prices["trend_price"])
                card.price_trend.append(new_price_trend)
                new_avg_1_price = Avg1Day(date=today, price=all_prices["avg_1_price"])
                card.avg_1_day.append(new_avg_1_price)
                new_avg_7_price = Avg7Days(date=today, price=all_prices["avg_7_price"])
                card.avg_7_days.append(new_avg_7_price)
                new_avg_30_price = Avg30Days(date=today, price=all_prices["avg_30_price"])
                card.avg_30_days.append(new_avg_30_price)
                print(url)
                last_id += 1
                status.last_id = last_id
                self.session.commit()
        except Exception as e:
            print(e)
            self.session.rollback()
            return False
        status.finished = True
        self.session.commit()
        return True

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

if __name__ == "__main__":
    price_service = PriceService()
    price_service.set_new_prices()