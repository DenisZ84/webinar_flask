from . import db
import datetime


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    date = db.Column(db.DateTime())

    def __init__(self, email):
        self.email = email

    def to_dict(self):
        return {'id': self.id, 'email': self.email, 'is_active': self.active}


class Price(db.Model):
    __tablename__ = 'fuel_prices'
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(255))
    price = db.Column(db.Float())
    date = db.Column(db.DateTime())

    def to_dict(self):
        return {'id': self.id,
                'city_name': self.city_name,
                'price': self.price,
                'date': self.date.strftime('%d.%m.%Y')}