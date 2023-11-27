from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
Base = declarative_base()


class Price(Base):
    __tablename__ = 'fuel_prices'
    id = Column(Integer, primary_key=True)
    city_name = Column(String(255))
    price = Column(Float())
    date = Column(DateTime())


class PricesPipeline:
    def open_spider(self, spider):
        engine = create_engine('sqlite:///sqlite.db')
        Base.metadata.create_all(engine)
        self.session = Session(engine)
    
    def process_item(self, item, spider):
        price = Price(
                    city_name=item['city_name'],
                    price=item['price'],
                    date=item['date'],
        )
        self.session.add(price)
        self.session.commit()
        return item
    
    def close_spider(self, spider):
        self.session.close()
