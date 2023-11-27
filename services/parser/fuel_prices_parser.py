import logging
import re
from logging.handlers import RotatingFileHandler
import json
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(
    "parser_logger.log", maxBytes=50000000, backupCount=5
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

fuel_types = [
    {"name": "Unleaded Premium", "type": 4},
    {"name": "Diesel", "type": 1},
    {"name": "Unleaded Regular", "type": 2},
    {"name": "Undeaded Mid-Grade", "type": 3},
]

cities_data = [
    {
        "city_name": "Albuquerque",
        "slug": "albuquerque-nm",
        "coords": (35.0843859, -106.650422),
    },
    {"city_name": "Atlanta", "slug": "atlanta-ga", "coords": (33.7489954, -84.3879824)},
    {"city_name": "Boston", "slug": "boston-ma", "coords": (42.3600825, -71.0588801)},
    {
        "city_name": "Charlotte",
        "slug": "charlotte-nc",
        "coords": (35.2270869, -80.8431267),
    },
    {"city_name": "Chicago", "slug": "chicago-il", "coords": (41.8781136, -87.6297982)},
    {
        "city_name": "Cleveland",
        "slug": "cleveland-oh",
        "coords": (41.49932, -81.6943605),
    },
    {
        "city_name": "Dallas",
        "slug": "dallas-fort-worth-tx",
        "coords": (32.7766642, -96.79698789999999),
    },
    {"city_name": "Denver", "slug": "denver-co", "coords": (39.7392358, -104.990251)},
    {
        "city_name": "Detroit",
        "slug": "detroit-mi",
        "coords": (42.33142699999999, -83.0457538),
    },
    {
        "city_name": "Indianapolis",
        "slug": "indianapolis-in",
        "coords": (39.768403, -86.158068),
    },
    {
        "city_name": "Kansas city",
        "slug": "kansas-city-ks",
        "coords": (39.11553139999999, -94.62678729999999),
    },
    {
        "city_name": "Las Vegas",
        "slug": "las-vegas-nv",
        "coords": (36.1699412, -115.1398296),
    },
    {
        "city_name": "Los Angeles",
        "slug": "los-angeles-ca",
        "coords": (34.0522342, -118.2436849),
    },
    {
        "city_name": "Nashville",
        "slug": "nashville-tn",
        "coords": (36.1626638, -86.7816016),
    },
    {
        "city_name": "New Orleans",
        "slug": "new-orleans-la",
        "coords": (29.95106579999999, -90.0715323),
    },
    {
        "city_name": "New York",
        "slug": "new-york-city-ny",
        "coords": (40.7127753, -74.0059728),
    },
    {"city_name": "Omaha", "slug": "omaha-ne", "coords": (41.2565369, -95.9345034)},
    {"city_name": "Orlando", "slug": "orlando-fl", "coords": (28.5383355, -81.3792365)},
    {
        "city_name": "Phoenix",
        "slug": "phoenix-az",
        "coords": (33.4483771, -112.0740373),
    },
    {
        "city_name": "Portland",
        "slug": "portland-or",
        "coords": (45.5051064, -122.6750261),
    },
    {
        "city_name": "Richmond",
        "slug": "richmond-va",
        "coords": (37.5407246, -77.4360481),
    },
    {
        "city_name": "Salt Lake City",
        "slug": "salt-lake-city-ut",
        "coords": (40.7607793, -111.8910474),
    },
    {
        "city_name": "San Antonio",
        "slug": "san-antonio-tx",
        "coords": (29.4241219, -98.49362819999999),
    },
    {
        "city_name": "San Francisco",
        "slug": "san-francisco-ca",
        "coords": (37.7749295, -122.4194155),
    },
    {
        "city_name": "Seattle",
        "slug": "seattle-wa",
        "coords": (47.6062095, -122.3320708),
    },
]

def parse_data(driver, security_code: str) -> None:
    for city in cities_data:
        for fuel in fuel_types:
            url = f"https://cstoredecisions.com/wp-admin/admin-ajax.php?action=get_rack_prices&security={security_code}&type={fuel['type']}&city={city['slug']}"
            logger.info("Request for prices...")
            logger.info(f'url: {url}')
            driver.get(url)
            logger.info("Request done")
            elements = driver.find_elements(By.TAG_NAME, "pre")
            if len(elements) == 0:
                error_message = "No json data found in response"
                logger.error(error_message)
                raise RuntimeError(error_message)
            data = json.loads(elements[0].text)
            price = data[-1][1]
            posix_date = int(str(data[-1][0])[:-3])
            price_date = datetime.datetime.fromtimestamp(posix_date)
            logger.info(f"Get for city: {city['city_name']} date:{price_date} price {price}$")
            

def start_parse():
    logger.debug("Стартуем парсер")
    with webdriver.Chrome() as browser:
        browser.get("https://cstoredecisions.com/rack-prices/?city=orlando-fl")
        result = re.findall('"rack_prices_nonce":"(\w+)"', browser.page_source)
        if len(result) > 0:
            security_code = result[0]
            logger.info(f"Код безопустности получен {security_code}")
        else:
            security_code = False
            error_message = "Does not get security code"
            logger.error(error_message)
            raise RuntimeError(error_message)
        parse_data(browser, security_code)


if __name__ == '__main__':
    start_parse()