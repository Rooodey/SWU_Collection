from models import Session, SWCards, CardQuantity
from .price_service import PriceService


class CardService:

    def __init__(self):
        self.session = Session()

    def set_sw_card(self, sw_set, number, variant, foil, name, german_name, subtitle, german_subtitle,
                    rarity, type, card_url, image_url):
        new_card = SWCards(
            set=sw_set,
            number=number,
            variant=variant,
            foil=foil,
            name=name,
            german_name=german_name,
            subtitle=subtitle,
            german_subtitle=german_subtitle,
            rarity=rarity,
            type=type,
            card_url=card_url,
            image_url=image_url
        )
        self.session.add(new_card)
        try:
            self.session.commit()
        except Exception as e:
            print(e)
            self.session.rollback()
            return None
        return new_card

    def get_all_sw_cards(self):
        all_cards = self.session.query(SWCards).all()
        return all_cards

    def get_sw_card_by_id(self, id):
        card = self.session.query(SWCards).filter_by(id=id).first()
        return card

    def get_value_of_owned_cards(self, user_id):
        cards = self.session.query(SWCards).all()
        total_value = 0
        for card in cards:
            price_service = PriceService()
            latest_avg_7_days_price = price_service.get_latest_avg_7_price(card)
            if latest_avg_7_days_price:
                card_quantity = self.session.query(CardQuantity) \
                    .filter_by(user_id=user_id, card_id=card.id) \
                    .first()
                total_value += card_quantity.quantity * latest_avg_7_days_price
        return total_value


if __name__ == "__main__":
    service = CardService()
