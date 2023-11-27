import scrapy
import re
import datetime

from get_prices_scrapy.items import PricesItem

fuel_types = [
    {"name": "Unleaded Premium", "type": 4},
    {"name": "Diesel", "type": 1},
    {"name": "Unleaded Regular", "type": 2},
    {"name": "Undeaded Mid-Grade", "type": 3},
]


class CstoredecisionsSpider(scrapy.Spider):
    name = "cstoredecisions"
    allowed_domains = ["cstoredecisions.com"]
    start_urls = ["https://cstoredecisions.com/rack-prices/?city=orlando-fl"]

    def parse(self, response):
        security_code = re.findall('"rack_prices_nonce":"(\w+)"', response.text)[0]
        city_option = response.xpath('//*[@id="rack-price-city"]/option/@value').getall()
        city_name = response.xpath('//*[@id="rack-price-city"]').css('option::text').getall()
        city_dict = dict(zip(city_name, city_option))
        for city_name, city_url in city_dict.items():
            for fuel in fuel_types:
                url = f"https://cstoredecisions.com/wp-admin/admin-ajax.php?action=get_rack_prices&security={security_code}&type={fuel['type']}&city={city_url}"
            yield response.follow(url, callback=self.parse_fuel, meta={'city_name':city_name})

        #return {'code': security_code, 'cities_list': city_dict}

    def parse_fuel(self, response):
        data = response.json()
        city_name = response.meta.get('city_name')
        posix_date = int(str(data[-1][0])[:-3])
        date = datetime.datetime.fromtimestamp(posix_date)
        price = data[-1][1]
        yield PricesItem({'city_name': city_name, 'date':date, 'price':price})