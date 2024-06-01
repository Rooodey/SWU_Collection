import json
import unicodedata
from datetime import date

from sqlalchemy import desc

from Cardmarket.database.init_db import get_session
from Cardmarket.database.models import SWCards, LowestPrice, PriceTrend, Avg1Day, Avg7Days, Avg30Days, UpdateStatus
from Cardmarket.services.crawler import *


class SWQueryService:
    """Service-Klasse für Abfragen und Änderungen an der StarWars-Datenbank."""

    def __init__(self):
        """Initialisiert die Datenbankverbindung."""
        self.session = get_session()

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

    def set_cards_from_json(self, json_file_path):
        with open(json_file_path, 'r') as file:
            sw_cards_json = json.load(file)
            sw_cards = sw_cards_json["data"]
            for card in sw_cards:
                if card["Rarity"] not in ["Common", "Uncommon"] or card["VariantType"] == "Showcase":
                    for i in range(2):
                        if (i == 1 and
                                (card["Type"] == "Leader"
                                 or card["Rarity"] == "Special"
                                 or card["Type"] == "Base" and card["Rarity"] != "Rare")):
                            continue
                        else:
                            card_url = self.create_url(
                                name=card["Name"],
                                subtitle=card.get("Subtitle"),
                                variant=card["VariantType"],
                                is_foil=i == 1,
                                type=card["Type"],
                                rarity=card["Rarity"]
                            )
                            german_name, german_subtitle = get_german_price_from_url(card_url)
                            self.set_sw_card(
                                sw_set=card["Set"],
                                number=card["Number"],
                                variant=card["VariantType"],
                                foil=i == 1,
                                name=card["Name"],
                                german_name=german_name,
                                subtitle=card.get("Subtitle"),
                                german_subtitle=german_subtitle,
                                rarity=card["Rarity"],
                                type=card["Type"],
                                card_url=card_url,
                                image_url=card["FrontArt"]
                            )

    def get_all_sw_cards(self):
        all_cards = self.session.query(SWCards).all()
        return all_cards

    def get_sw_card_by_id(self, id):
        card = self.session.query(SWCards).filter_by(id=id).first()
        return card

    def get_value_of_owned_cards(self):
        cards = self.session.query(SWCards).all()
        total_value = 0
        for card in cards:
            latest_avg_7_days_price = self.session.query(Avg7Days).filter(Avg7Days.card_id == card.id).order_by(
                desc(Avg7Days.date)).first()
            if latest_avg_7_days_price:
                total_value += card.amount * latest_avg_7_days_price.price
        return total_value

    @staticmethod
    def create_url(name: str, subtitle: str, variant: str, is_foil: bool, type: str, rarity: str):
        nfkd_form = unicodedata.normalize('NFKD', name)
        name = ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
        new_name = name.replace(" ", "-").replace("'", "").replace("\"", "")
        if type != "Base":
            if subtitle:
                new_subtitle = subtitle.replace(" ", "-").replace("'", "").replace("\"", "")
                new_name += f"-{new_subtitle}"
        elif rarity != "Rare":
            new_name += f"-experience-token"
        hs = ""
        extra = ""
        foil = ""
        if variant in ["Hyperspace", "Showcase"]:
            hs = "-Extras"
        if variant == "Hyperspace" and type == "Leader":
            extra = "-V1"
        if variant == "Showcase":
            extra = "-V2"
        if is_foil:
            foil = "?isFoil=Y"
        if (variant == "Normal" and
                ((name == "Emperor Palpatine" and subtitle == "Master of the Dark Side")
                 or (name == "Han Solo" and subtitle == "Reluctant Hero")
                 or (name == "Obi-Wan Kenobi" and subtitle == "Following Fate")
                 or (name == "Relentless" and subtitle == "Konstantine's Folly"))):
            extra = "-V1"
        return (f"https://www.cardmarket.com/de/StarWarsUnlimited/Products/Singles/Spark-of-Rebellion{hs}/{new_name}"
                f"{extra}{foil}")

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
            return str(latest_avg_7_days_price.price) + "€"
        return None

    def get_lowest_price(self, card):
        latest_lowest_price = self.session.query(LowestPrice).filter(LowestPrice.card_id == card.id).order_by(
            desc(LowestPrice.date)).first()
        if latest_lowest_price:
            return str(latest_lowest_price.price) + "€"
        return None

    def update_amount_by_id(self, id, new_amount):
        card = self.session.query(SWCards).filter_by(id=id).first()
        card.amount = new_amount
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
            return False
        return True



if __name__ == "__main__":
    service = SWQueryService()
    # service.set_cards_from_json("../files/sor.json")
    print(service.set_new_prices())
