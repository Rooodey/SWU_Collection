from bs4 import BeautifulSoup
import cloudscraper
import time
import random


def error_handling(func):
    def wrapper(url):
        scraper = cloudscraper.create_scraper()
        max_retries = 3
        for i in range(max_retries):
            try:
                time.sleep(random.randint(1, 3))
                return func(scraper, url)
            except (ValueError, AttributeError) as e:
                print(f"Attempt {i + 1} failed: {e}")
            except Exception as e:
                print(f"Attempt {i + 1} failed: {e}")
                time.sleep(5)
        raise ValueError(f"Failed to get the price after {max_retries} attempts")
    return wrapper

@error_handling
def get_price_from_url(scraper, url):
    response = scraper.get(url, timeout=5)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    price_names = [
        "ab",
        "Preis-Trend",
        "1-Tages-Durchschnitt",
        "7-Tages-Durchschnitt",
        "30-Tages-Durchschnitt"
    ]
    dt = soup.find(string=price_names[0])
    lowest_price = get_price_from_dt(dt, price_names[0])
    dt = soup.find(string=price_names[1])
    price_trend = get_price_from_dt(dt, price_names[1])
    dt = soup.find(string=price_names[2])
    avg_1_price = get_price_from_dt(dt, price_names[2])
    dt = soup.find(string=price_names[3])
    avg_7_price = get_price_from_dt(dt, price_names[3])
    dt = soup.find(string=price_names[4])
    avg_30_price = get_price_from_dt(dt, price_names[4])
    return dict(lo_price=lowest_price, trend_price=price_trend, avg_1_price=avg_1_price,
                avg_7_price=avg_7_price, avg_30_price=avg_30_price)


def get_price_from_dt(dt, price_name):
    if dt is None:
        raise ValueError(f"Could not find the element with the text: {price_name}")
    price = dt.findNext("dd")
    if price is None:
        raise ValueError(f"Could not find the 'dd' element following the text: {price_name}")
    price_str = price.get_text()
    cleaned_price_str = "".join(char for char in price_str.replace(",", ".") if char.isdigit() or char == ".")
    return float(cleaned_price_str)

@error_handling
def get_german_price_from_url(scraper, url):
    response = scraper.get(url, timeout=5)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    h1_tag = soup.find("h1")
    span = h1_tag.find('span')
    span.decompose()
    h1_list = [text.strip() for text in h1_tag.text.split(",")]
    if len(h1_list) < 2:
        h1_list.append(None)
    return tuple(h1_list)

if __name__ == "__main__":
    test = get_german_price_from_url("https://www.cardmarket.com/de/StarWarsUnlimited/Products/Singles/Spark-of-Rebellion/Admiral-Ackbar-Brilliant-Strategist?isFoil=Y")
    print(test)
