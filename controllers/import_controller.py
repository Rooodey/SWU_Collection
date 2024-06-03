import json
import unicodedata
from SWU_Collection.crawler import get_german_name_from_url
from SWU_Collection.services import CardService

def set_cards_from_json(json_file_path):
    service = CardService()
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
                        card_url = create_url(
                            name=card["Name"],
                            subtitle=card.get("Subtitle"),
                            variant=card["VariantType"],
                            is_foil=i == 1,
                            type=card["Type"],
                            rarity=card["Rarity"]
                        )
                        german_name, german_subtitle = get_german_name_from_url(card_url)
                        service.set_sw_card(
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